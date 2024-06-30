from pyspark import SparkConf, SparkContext
import sys,time


if __name__ == "__main__":
    conf = SparkConf().setAppName("RootFinding")
    sc = SparkContext(conf = conf)
    start_time = time.time()
    path = "/user/yjagilan/A2/input.txt"
    lines = sc.textFile(path)
    # lines = sc.textFile(sys.argv[1])

    rdd1 = lines.flatMap(lambda line : [[int(x) for x in line.split(" ")]]).groupByKey().mapValues(list)
    rdd2 = rdd1.flatMap(lambda line : [[line[1][0],line[0]]]).groupByKey().mapValues(list)
    result = sc.union([rdd1,rdd2]).groupByKey().mapValues(list).flatMap(lambda test : [ [x,test[1][0][0]] for x in test[1][1] ] if len(test[1])>1 else [] )
    
    previous_count = result.values().sum()
    current_count= 0
    
    while( current_count != previous_count):
        previous_count = current_count
        rdd1 = result.groupByKey().mapValues(list)
        rdd2 = result.flatMap(lambda x: [x[::-1]]).groupByKey().mapValues(list)
        result = sc.union([rdd1,rdd2]).groupByKey().mapValues(list).flatMap(lambda test : [ [x,test[1][0][0]] for x in test[1][1] ] if len(test[1])>1 else [] )
        current_count = result.values().sum()

    # result.saveAsTextFile(sys.argv[2])  
    result.saveAsTextFile("output")   
    sc.stop()
    print(time.time()-start_time)