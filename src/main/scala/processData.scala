import org.apache.log4j.{Level, LogManager, Logger}
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{StringType, StructField, StructType}




object processData {
  def main(args: Array[String]): Unit ={
    LogManager.getLogger("org").setLevel(Level.OFF)
    LogManager.getLogger("akka").setLevel(Level.OFF)

    val spark = SparkSession.builder().appName("dataProcessing").master("local[*]").getOrCreate()

    // For implicit conversions like converting RDDs to DataFrames
    import spark.implicits._

    val schemaTyped = new StructType()
      .add("Headline", StringType)
      .add("Date", StringType)

    val df = spark.read.option("delimiter","|").schema(schemaTyped).csv("data/NYT_ArticlesTXT/")
    df.show()
    print(df.count())

  }
}