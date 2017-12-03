import org.apache.log4j.{Level, LogManager}
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
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
        concat_ws(" ", collect_list("Headline")) as "Headlines"
      )


    /* Processing for Stock Symbol History */
    val schemaStock = new StructType()
      .add("Date", StringType)
      .add("Open", DoubleType)
      .add("High", DoubleType)
      .add("Low", DoubleType)
      .add("Close", DoubleType)
      .add("Volume", LongType)
    val STOCK_HISTORY = spark.read.option("header","true").schema(schemaStock).csv("data/Stock_Prices")


    /* Joining NYT Articles with Stock History */
    var NYT_AND_STOCK = NYTHeadlinesGrouped.join(STOCK_HISTORY,"Date")
    NYT_AND_STOCK = NYT_AND_STOCK.sort("Date")
    //println(NYT_AND_STOCK.count())
    NYT_AND_STOCK.show()

    NYT_AND_STOCK.coalesce(1).write.option("header",true).csv("data/NYT_STOCK")

    spark.close()


    /* Renaming CSV File */
    val conf = new SparkConf().setAppName("dataProcessing").setMaster("local[*]")
    val sc = new SparkContext(conf)

    import org.apache.hadoop.fs._
    import org.apache.hadoop.fs.FileSystem
    val fs = FileSystem.get(sc.hadoopConfiguration)
    val file = fs.globStatus(new Path("data/NYT_STOCK/part*"))(0).getPath().getName()

    fs.rename(new Path("data/NYT_STOCK/" + file), new Path("data/NYT_STOCK/totalData.csv"))
    fs.delete(new Path("mydata.csv-temp"), true)


  }
}