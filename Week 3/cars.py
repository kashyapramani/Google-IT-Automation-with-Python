#!/usr/bin/env python3

import json
import locale
import sys
import os
import reports
import emails


def load_data(filename):
    """Loads the contents of filename as a JSON file."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def format_car(car):
    """Given a car dictionary, returns a nicely formatted name."""
    return "{} {} ({})".format(
        car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
    """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    max_revenue = {"revenue": 0}
    most_sales = {"total_sales": 0}
    popular = {}

    for item in data:
        # Calculate the revenue generated by this model (price * total_sales)
        # We need to convert the price from "$1234.56" to 1234.56
        item_price = locale.atof(item["price"].strip("$"))
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item
        # TODO: also handle max sales

        if item["total_sales"] > most_sales["total_sales"]:
            most_sales = item

        # TODO: also handle most popular car_year

        if item["car"]["car_year"] not in popular:
            popular[item["car"]["car_year"]] = item["total_sales"]
        else:
            popular[item["car"]["car_year"]] += item["total_sales"]

        # years = popular.keys()
        # sales = popular.values()
        # max_sale = max(sales)
        # year = years[sales.index(max_sale)]

        max_sale = max(popular.values())
        year = max(popular, key=popular.get)

    summary = [
        "The {} generated the most revenue: ${}".format(
            format_car(max_revenue["car"]), max_revenue["revenue"]),
        "The {} had the most sales: {}".format(most_sales["car"]["car_model"], most_sales["total_sales"]),
        "The most popular year was {} with {} sales.".format(year, max_sale),
    ]

    return summary


def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists."""
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
    return table_data


def main(argv):
    """Process the JSON data and generate a full report out of it."""
    data = load_data("car_sales.json")
    summary = process_data(data)

    # TODO: turn this into a PDF report
    path = "/tmp/cars.pdf"
    title = "Final Report of Cars"
    report_content = '<br/>'.join(summary)
    table_data = cars_dict_to_table(data)

    reports.generate(path, title, report_content, table_data)

    # TODO: send the PDF report as an email attachment
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.getenv('USER'))
    subject = "Sales summary for last month"
    email_content = '\n'.join(summary)

    msg = emails.generate(sender, receiver, subject, email_content, path)
    emails.send(msg)


if __name__ == "__main__":
    main(sys.argv)
