import org.apache.log4j.{Level, LogManager}
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.functions.{array, collect_list}
import org.apache.spark.sql.functions._



object processData {
  def main(args: Array[String]): Unit ={
    LogManager.getLogger("org").setLevel(Level.OFF)
    LogManager.getLogger("akka").setLevel(Level.OFF)

    val spark = SparkSession.builder().appName("dataProcessing").master("local[*]").getOrCreate()


    /* Processing for NYT Headlines */
    val schemaNYT = new StructType()
      .add("Headline", StringType)
      .add("Date", StringType)

    val NYT_Articles = spark.read.option("delimiter","|").schema(schemaNYT).csv("data/NYT_ArticlesTXT/")
    val noNullsNYT = NYT_Articles.na.drop()


    val NYTHeadlinesGrouped  = noNullsNYT.groupBy("Date")
      .agg(
        collect_list("Headline") as "Headlines"
      )


    /* Processing for Stock Symbol History */
    val schemaStock = new StructType()
      .add("TimeStamp", StringType)
      .add("Open", DoubleType)
      .add("High", DoubleType)
      .add("Low", DoubleType)
      .add("Close", DoubleType)
      .add("Volume", LongType)

    val STOCK_HISTORY = spark.read.option("header","true").schema(schemaStock).csv("data/Stock_Prices")
    STOCK_HISTORY.show(false)

  }
}