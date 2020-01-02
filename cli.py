"""
What is needed for click module

List of Regions

List of Sancuaries

Start Date / end Date

Age Filter (Multi Select)

    All
    Families
    Children
    Teens
    Adults

Schedule Filter (Multi Select)

    Weekday
    Weeknight
    Weekends
    Trips


order =

location

audience

schedule

start_date

end_date

Total Events to show
"""

import click
from datetime import datetime, timedelta
from scraper import AudobonScraper

@click.command()
@click.option('--location', default='greater-boston', help='Enter Audobon Region or a specific sanctuary')
@click.option('--start_date', default=datetime.today().strftime('%m-%d-%Y'), help='Start date for event filter')
@click.option('--end_date', default=str((datetime.today() + timedelta(30)).strftime('%m-%d-%Y')), help='End date for event filter')
@click.argument('filters', nargs=-1)
def cli(location, start_date, end_date, filters):
    search_url = build_url(location,start_date, end_date, filters)
    scraper = AudobonScraper(url=search_url)
    events = scraper.run()
    print(events[1])
    print(len(events))



def build_url(location, start_date, end_date, filters):
    filter_dict = {'all': 'all-audiences',
                'family': 'family',
                'children': 'children',
                'teens': 'teens',
                'adults': 'adults',
                }
    #daytime-weekdays/evening-weekdays/weekends/overnight-trips/


    if filters:
        formatted_filters = '/'.join(filters[1:])
        search_url = f"/{location}/{formatted_filters}/(startDate)/{start_date}/(endDate)/{end_date}/(offset)/0/(limit)/500"
    else:
        search_url = f"/{location}/(startDate)/{start_date}/(endDate)/{end_date}(offset)/0/(limit)/500"
    print(search_url)
    return search_url


if __name__ == '__main__':
    cli()



