#extract_timeseries.py

import sys
import csv
import os

def read_metric_values(metric, column_index, releases, input):
    
    print("Reading " + metric.upper() + " values...")

    results = dict()
    for release in list(range(int(releases))):
    
        release_index = release + 1
        path = input + "/" + str(release_index) + "/class.csv" if not input.endswith('/') else input + str(release_index) + "/class.csv"
        
        print("Reading release " + str(release_index) + " from the project...")

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:

                    package_test = "." + row[1].rsplit(", ", 1)[0] + "."
                    if (".test." not in package_test.lower()) and (".tests." not in package_test.lower()):
                    
                        if row[1] not in results:
                            results[row[1]] = dict()
                        
                        results[row[1]][release_index] = row[column_index]

                line_count = line_count + 1

    print("Finished reading!")

    return results

def export_timeseries(metric, column_index, releases, timeseries_output, metric_data):
    
    print("Exporting " + metric.upper() + " timeseries...")
    
    csv_name = timeseries_output + metric + ".csv"

    with open(csv_name, mode='w') as timeserie_file:
        writer = csv.writer(timeserie_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for key in metric_data:
            line = [key]
            
            for release in list(range(int(releases))):

                release_index = release + 1
                if release_index in metric_data[key]:
                    line.append(metric_data[key][release_index])
                else: 
                    if metric == 'lcom':
                        line.append("-1.0")
                    else:
                        line.append("-1")
            
            writer.writerow(line)
    print(metric.upper() + " timeseries exported!")



def generate_timeseries(input, output):

    metrics_index = get_metrics(input)
    metrics = metrics_index['metrics']
    indexColuns = metrics_index['index']

    number_releases = get_release_numbers(input)

    print("---------------------------------- Starting the process of reading and exporting of the project timeseries release ----------------------------------\n")

    for i in list(range(len(indexColuns))):
        
        metric_data = read_metric_values(metrics[i], indexColuns[i], number_releases, input)

        name_project = input.rsplit("/", 1)[1] if not input.endswith('/') else input.rsplit("/", 2)[1]
        timeseries_output = output + "/" + name_project + "/" if not input.endswith('/') else output + name_project + "/"

        if not os.path.exists(timeseries_output):
                os.makedirs(timeseries_output)

        export_timeseries(metrics[i], indexColuns[i], number_releases, timeseries_output, metric_data)

    print("\nTime series generation completed!")



def get_release_numbers(input):
    number_releases = 0
    for f in os.listdir(input):
        if "_" not in f:
            number_releases = number_releases + 1
    
    return number_releases



def get_metrics(input):
    metrics_index = dict()
    metrics = []
    index = []

    input = input + "/1/class.csv" if not input.endswith('/') else input + "1/class.csv"

    columns = ""
    with open(input, 'r') as csv_file:
        d_reader = csv.DictReader(csv_file)
        columns = d_reader.fieldnames

    count = 0
    for c in columns:
        if(c != 'file' and c != 'class' and c != 'type'):
            metrics.append(c)
            index.append(count)
        
        count = count + 1
    
    metrics_index["metrics"] = metrics
    metrics_index["index"] = index
    return metrics_index


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 3:
        print("Usage python3 extract_timeseries.py <directory of the versions with system metrics> <path to save the output files>")
    else:
        generate_timeseries(args[1], args[2])
