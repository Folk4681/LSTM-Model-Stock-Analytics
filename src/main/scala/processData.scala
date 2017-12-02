import org.apache.log4j.{Level, LogManager, Logger}
import org.apache.spark._
import org.apache.spark.sql.SparkSession




object ProcessData {
  def main(args: Array[String]): Unit ={
    LogManager.getLogger("org").setLevel(Level.OFF)
    LogManager.getLogger("akka").setLevel(Level.OFF)

    val spark = SparkSession.builder().appName("dataProcessing").master("local[*]").getOrCreate()

    // For implicit conversions like converting RDDs to DataFrames
    import spark.implicits._

    val df = spark.read.json("data/NYT_Articles/2016-1.json")
    df.select("response").show(1)
  }
}