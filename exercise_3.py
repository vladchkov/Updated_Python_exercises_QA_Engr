import csv
from datetime import datetime
from http import HTTPStatus

import tzlocal


def parse_jmeter_logs(file_name: str) -> None:
    """
    Parses jmeter log file for non-successful endpoint responses
    Prints out the label, response code, response message, failure message,
    and the time of non-200 response in human-readable format in PST timezone

    :param file_name: jmeter log file
    :return: None
    """
    if not file_name:
        return

    time_stamp_ind = None
    label_ind = None
    response_code_ind = None
    response_message_ind = None
    failure_message_ind = None

    with open(file_name) as csvfile:
        jmeter_logs = csv.reader(csvfile, delimiter=',')

        for row in jmeter_logs:
            time_stamp_ind = row.index("timeStamp")
            label_ind = row.index("label")
            response_code_ind = row.index("responseCode")
            response_message_ind = row.index("responseMessage")
            failure_message_ind = row.index("failureMessage")
            break

        for row in jmeter_logs:
            if int(row[response_code_ind]) != HTTPStatus.OK:
                local_timezone = tzlocal.get_localzone()
                record_datetime = datetime.fromtimestamp(
                    int(row[time_stamp_ind]) / 1000, local_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
                print(record_datetime, row[label_ind], row[response_code_ind],
                      row[response_message_ind], row[failure_message_ind])


if __name__ == "__main__":
    parse_jmeter_logs('Jmeter_log1.jtl')
    parse_jmeter_logs('Jmeter_log2.jtl')
