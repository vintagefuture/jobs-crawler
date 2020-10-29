import scrapy
from jobs.items import JobsItem


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['indeed.co.uk']
    start_urls = ['https://www.indeed.co.uk/jobs?q=system+administrator&l=Edinburgh%2C+City+of+Edinburgh']

    def parse(self, response):
        job_cards = response.xpath("//*[contains(@class, 'jobsearch-SerpJobCard unifiedRow row result')]")

        for card in job_cards:
            title = card.css('a::attr(title)')[0].get()
            url = card.css('a::attr(href)')[0].get()
            url = 'https://indeed.co.uk' + url
            salary = card.css('span.salaryText::text').get()
            description = ' '.join(card.css('div.summary').css('li::text').getall())

            job = JobsItem(
                title=title,
                url=url,
                salary=salary,
                description=description,
            )

            yield job

        pages = response.css('ul.pagination-list').css('li')
        next_url = pages[-1].css('a::attr(href)').get()
        next_url = 'https://indeed.co.uk' + next_url

        yield scrapy.Request(
            url=next_url,
        )
