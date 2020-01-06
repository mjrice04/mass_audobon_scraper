import click
from datetime import datetime, timedelta
from scraper import AudobonScraper
from send_email import send_email, handle_events

@click.command()
@click.option('--location', default='greater-boston', help='Enter Audobon Region or a specific sanctuary')
@click.option('--start_date', default=datetime.today().strftime('%m-%d-%Y'), help='Start date for event filter')
@click.option('--end_date', default=str((datetime.today() + timedelta(30)).strftime('%m-%d-%Y')), help='End date for event filter')
@click.argument('filters', nargs=-1)
def cli(location, start_date, end_date, filters):
    """
    Click cmd line tool to parameterize the filters for mass audobon events
    Ex: python cli.py --location greater_boston --start_date 12-31-2019 --end_date 12-31-2020 filters all-audiences weekends
    :param location: What location to parse events from
    :param start_date: Start date to parse
    :param end_date: End date to parse
    :param filters: specific age group and time of event filters to pass in
    :return:
    """
    search_url = build_url(location,start_date, end_date, filters)
    scraper = AudobonScraper(url=search_url)
    events = scraper.run()
    formatted_message = []
    for event in events:
        message = handle_events(event)
        formatted_message.append(message)
    email_message = '\n'.join(formatted_message)
    send_email(email_message)


def build_url(location, start_date, end_date, filters):
    """
    Builds the url to scrape with passed in parameters from command
    :param location: what location to parse events from
    :param start_date: start date to parse
    :param end_date: end date to parse
    :param filters: search filters for events for target age for event to time of week. All examples below
    all-audiences, family, children, teens, adults, daytime-weekdays, evening-weekdays, weekends, overnight-trips
    :return:
    """
    # if filters is not blank add the filters to the url to be scraped
    if filters:
        formatted_filters = '/'.join(filters[1:])
        search_url = f"/{location}/{formatted_filters}/(startDate)/{start_date}/(endDate)/{end_date}/(offset)/0/(limit)/500"
    else:
        search_url = f"/{location}/(startDate)/{start_date}/(endDate)/{end_date}(offset)/0/(limit)/500"
    return search_url


if __name__ == '__main__':
    cli()



