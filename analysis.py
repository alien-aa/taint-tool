import subprocess
import sys
import os
import re
import csv

def output_to_csv(output_filename_):
    """
    Tabulating data
    """

    csv_filename = "results.csv"
    leaks = []
    sinks_flag = 0

    with open(output_filename_, 'r', encoding='utf-8') as f:
        for line in f:
            if sinks_flag:
                sinks_flag = 0
                parts = line.split(' - - ')
                sources = parts[1].strip()
                leak_info = {
                    "Sink": sink,
                    "Sources": sources
                }
                leaks.append(leak_info)
            if line.startswith("[main] INFO soot.jimple.infoflow.android.SetupApplication$InPlaceInfoflow - The sink"):
                sinks_flag = 1
                parts = line.split(' - The sink ')
                sink = parts[1].strip()
                parts = sink.split(' was called with values from the following sources:')
                sink = parts[0].strip()
            if line.startswith("[main] INFO soot.jimple.infoflow.android.SetupApplication - Found"):
               number_of_leaks = re.search(r"Found (\d+) leaks", line).group(1)

    with open(csv_filename, "a+") as csvfile:
        csvfile.seek(0)
        if os.stat(csv_filename).st_size != 0:
            csvfile.seek(0, os.SEEK_END)
        writer = csv.DictWriter(csvfile, fieldnames=["Sink", "Sources"], restval="")
        writer.writerow({"Sink": "Number of leaks", "Sources": number_of_leaks})
        writer.writeheader()
        for item in leaks:
            writer.writerow(item)
    
    

def run_analysis(apk_path, platform_tools_path, sources_and_sinks_path):
  """
  Starting the analysis, writing data to a file 
  """

  command = [
      "java", "-jar", 
      os.getcwd() + "\\FlowDroid-2.13\\soot-infoflow-cmd\\target\\soot-infoflow-cmd-jar-with-dependencies.jar",
      "-a", apk_path, 
      "-p", platform_tools_path, 
      "-s", sources_and_sinks_path
  ] 

  output_filename = "output.txt"

  if not os.path.exists(output_filename):
      with open(output_filename, "w", encoding='utf-8') as output_file:
          process = subprocess.run(command, stdout=output_file, stderr=output_file)
  else:
      with open(output_filename, "a", encoding='utf-8') as output_file:
          process = subprocess.run(command, stdout=output_file, stderr=output_file)
  if process.returncode == 0:
      output_to_csv(output_filename)
      print(f"Анализ завершен успешно. Вывод записан в {output_filename}.")
  else:
      print(f"Ошибка при запуске анализа. Проверьте {output_filename}.")



def parse_arguments(args):
    """
    Processing command line arguments
    """
    parsed_args = {
        "apk_path": None,
        "platform_tools_path": os.getcwd() + "\\platform-tools",  
        "sources_and_sinks_path": os.getcwd() + "\\FlowDroid-2.13\\soot-infoflow-android\\SourcesAndSinks.txt"  
    }

    i = 1
    while i < len(args):
        arg = args[i]
        if arg == "-apk":
            parsed_args["apk_path"] = args[i+1]
            i += 2
        elif arg == "-p":
            parsed_args["platform_tools_path"] = args[i+1]
            i += 2
        elif arg == "-s":
            parsed_args["sources_and_sinks_path"] = args[i+1]
            i += 2
        else:
            i += 1

    return parsed_args



def help():
    print("Использование: python analysis.py <apk_path> [-p <platform_tools_path>] [-s <sources_and_sinks_path>]")
    print("<apk_path> - путь к APK-файлу (например, C:\\Users\\User\\Downloads\\myapp.apk)")
    print("<platform_tools_path> - путь к папке platform-tools (например, C:\\Users\\User\\projects\\taint_analysis\\platform-tools)")
    print("<sources_and_sinks_path> - путь к файлу SourcesAndSinks.txt (например, C:\\Users\\User\\projects\\taint_analysis\\FlowDroid-2.13\\soot-infoflow-android\\SourcesAndSinks.txt)")
    


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        help()
    else:
        parsed_args = parse_arguments(sys.argv)

        apk_path = parsed_args["apk_path"]
        platform_tools_path = parsed_args["platform_tools_path"]
        sources_and_sinks_path = parsed_args["sources_and_sinks_path"]

        if apk_path is None:
            print("Необходимо указать путь к APK-файлу.")
            help()
        else:
            run_analysis(apk_path, platform_tools_path, sources_and_sinks_path)
            