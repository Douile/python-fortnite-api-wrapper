from . import constants, utils


class Base:
    def __init__(self, response):
        self.response = response


class Player(Base):
    def __init__(self, response):
        super().__init__(response)
        self.name = self.response.get('displayName')
        self.id = self.response.get('id')

    def __iter__(self):
        yield 'name', self.name
        yield 'id', self.id


class BattleRoyale(Base):
    def __init__(self, response, platform):
        super().__init__(response)
        self.solo = BattleRoyaleStats(response=self.response, platform=platform, mode='_p2')
        self.duo = BattleRoyaleStats(response=self.response, platform=platform, mode='_p10')
        self.squad = BattleRoyaleStats(response=self.response, platform=platform, mode='_p9')
        self.all = BattleRoyaleStats(response=self.response, platform=platform, mode='_p')

    def __iter__(self):
        yield 'solo', dict(self.solo)
        yield 'duo', dict(self.duo)
        yield 'squad', dict(self.squad)
        yield 'all', dict(self.all)


class BattleRoyaleStats(Base):
    def __init__(self, response, platform, mode):
        super().__init__(response)
        self.score = 0
        self.matches = 0
        self.time = 0
        self.kills = 0
        self.wins = 0
        self.top3 = 0
        self.top5 = 0
        self.top6 = 0
        self.top10 = 0
        self.top12 = 0
        self.top25 = 0
        for stat in self.response:
            if platform in stat.get('name') and mode in stat.get('name'):
                if 'score_' in stat.get('name'):
                    self.score += stat.get('value')
                elif 'matchesplayed_' in stat.get('name'):
                    self.matches += stat.get('value')
                elif 'minutesplayed_' in stat.get('name'):
                    self.time += stat.get('value')
                elif 'kills_' in stat.get('name'):
                    self.kills += stat.get('value')
                elif 'placetop1_' in stat.get('name'):
                    self.wins += stat.get('value')
                elif 'placetop3_' in stat.get('name'):
                    self.top3 += stat.get('value')
                elif 'placetop5_' in stat.get('name'):
                    self.top5 += stat.get('value')
                elif 'placetop6_' in stat.get('name'):
                    self.top6 += stat.get('value')
                elif 'placetop10_' in stat.get('name'):
                    self.top10 += stat.get('value')
                elif 'placetop12_' in stat.get('name'):
                    self.top12 += stat.get('value')
                elif 'placetop25_' in stat.get('name'):
                    self.top25 += stat.get('value')

    def __iter__(self):
        yield 'score', self.score
        yield 'matches', self.matches
        yield 'time', self.time
        yield 'kills', self.kills
        yield 'wins', self.wins
        yield 'top3', self.top3
        yield 'top5', self.top5
        yield 'top6', self.top6
        yield 'top10', self.top10
        yield 'top12', self.top12
        yield 'top25', self.top25


class Store(Base):
    def __init__(self, response):
        super().__init__(response)
        self.refresh_interval_hrs = self.response.get('refreshIntervalHrs')
        self.daily_purchase_hrs = self.response.get('dailyPurchaseHrs')
        self.expiration = self.response.get('expiration')
        self.storefronts = self.storefront_list()

    def storefront_list(self):
        return [StoreFront(response) for response in self.response.get('storefronts')]

    def __iter__(self):
        yield 'storefronts', utils.dict_array(self.storefronts)
        yield 'expiration', self.expiration
        yield 'dailyPurchaseHrs', self.daily_purchase_hrs
        yield 'refreshIntervalHrs', self.refresh_interval_hrs


class StoreFront(Base):
    def __init__(self, response):
        super().__init__(response)
        self.name = self.response.get('name')
        self.catalog_entries = self.catalog_entry_list()

    def catalog_entry_list(self):
        return utils.class_array(CatalogEntry, self.response.get('catalogEntries'))

    def __iter__(self):
        yield 'name', self.name
        yield 'catalogEntries', utils.dict_array(self.catalog_entries)


class CatalogEntry(Base):
    def __init__(self, response):
        super().__init__(response)
        self.offer_id = self.response.get('offerId')
        self.dev_name = self.response.get('devName')
        self.offer_type = self.response.get('offerType')
        self.prices = self.price_list()
        self.title = self.response.get('title')
        self.description = self.response.get('description')
        self.refundable = self.response.get('refundable')

    def price_list(self):
        return [Price(response) for response in self.response.get('prices')]

    def __iter__(self):
        yield 'offerId', self.offer_id
        yield 'devName', self.dev_name
        yield 'offerType', self.offer_type
        yield 'prices', self.prices
        yield 'title', self.title
        yield 'description', self.description
        yield 'refundable', self.refundable


class Price(Base):
    def __init__(self, response):
        super().__init__(response)
        self.currency_type = self.response.get('currencyType')
        self.regular_price = self.response.get('regularPrice')
        self.final_price = self.response.get('finalPrice')
        self.sale_expiration = self.response.get('saleExpiration')
        self.base_price = self.response.get('basePrice')

    def __iter__(self):
        yield 'currencyType', self.currency_type
        yield 'regularPrice', self.regular_price
        yield 'finalPrice', self.final_price
        yield 'saleExpiration', self.sale_expiration
        yield 'basePrice', self.base_price


class News(Base):
    def __init__(self, response):
        super().__init__(response)

        common = response.get('athenamessage').get('overrideablemessage')
        if common.get('message') is not None:
            self.common = utils.class_array(NewsMessage, [common.get('message')])
        elif common.get('messages') is not None:
            self.common = utils.class_array(NewsMessage, common.get('messages'))
        else:
            self.common = None

        br = response.get('battleroyalenews').get('news')
        if br.get('message') is not None:
            self.br = utils.class_array(NewsMessage, [br.get('message')])
        elif br.get('messages') is not None:
            self.br = utils.class_array(NewsMessage, br.get('messages'))
        else:
            self.br = None

        login = response.get('loginmessage').get('loginmessage')
        if login.get('message') is not None:
            self.login = utils.class_array(NewsMessage, [login.get('message')])
        elif login.get('messages') is not None:
            self.login = utils.class_array(NewsMessage, login.get('messages'))
        else:
            self.login = None

        emergency = response.get('emergencynotice').get('news')
        if emergency.get('message') is not None:
            self.emergency = utils.class_array(NewsMessage, [emergency.get('message')])
        elif emergency.get('messages') is not None:
            self.emergency = utils.class_array(NewsMessage, emergency.get('messages'))
        else:
            self.emergency = None

    def __iter__(self):
        yield 'status', self.status
        yield 'common', utils.dict_array(self.common)
        yield 'br', utils.dict_array(self.br)
        yield 'login', utils.dict_array(self.login)
        yield 'emergency', utils.dict_array(self.emergency)
        

class NewsMessage(Base):
    def __init__(self, response):
        super().__init__(response)
        self.image = self.response.get('image')
        self.title = self.response.get('title')
        self.body = self.response.get('body')


class PatchNotes(Base):
    def __init__(self, status, response):
        super().__init__(response)
        self.status = status

        self.post_count = response.get('postCount')
        self.increment_count = response.get('incrementCount')
        self.total_blogs = response.get('blogTotal')
        self.totals = CategoryTotals(response.get('categoryTotals'))
        self.blogs = utils.class_array(Blog, response.get('blogList'))

    def __iter__(self):
        yield 'status', self.status
        yield 'postCount', self.post_count
        yield 'incrementCount', self.increment_count
        yield 'totalBlogs', self.total_blogs
        yield 'totals', dict(self.totals)
        yield 'blogs', utils.dict_array(self.blogs)



class CategoryTotals:
    def __init__(self, data):
        self.community = data.get('community')
        self.events = data.get('events')
        self.patch_notes = data.get('patch_notes')
        self.announcements = data.get('announcements')
        self.all = data.get('all')

    def __iter__(self):
        yield 'community', self.community
        yield 'events', self.events
        yield 'patchNotes', self.patch_notes
        yield 'announcements', self.announcements
        yield 'all', self.all


class Blog:
    def __init__(self, data):
        self.trending = data.get('trending')
        self.no_top_image = data.get('noTopImage')
        self.image = data.get('image')
        self.author = data.get('author')
        self.share_image = data.get('shareImage')
        self.title = data.get('title')
        self.html_content = data.get('content')
        self.trending_image = data.get('trendingImage')
        self.category = data.get('cat')
        self.html_short = data.get('short')
        self.featured = data.get('featured')
        self.date = data.get('date')
        if self.date is not None:
            self.date = utils.convert_iso_time(self.date)
        self.id = data.get('_id')
        self.slug = data.get('slug')
        self.locale = data.get('locale')
        self.categories = data.get('category')
        self.tags = data.get('tags')
        if self.slug is not None and self.locale is not None:
            self.url = constants.blog.format(self.locale, self.slug)
        else:
            self.url = None

    def __iter__(self):
        yield 'trending', self.trending
        yield 'image', self.image
        yield 'author', self.author
        yield 'shareImage', self.share_image
        yield 'title', self.title
        yield 'htmlContent', self.html_content
        yield 'trendingImage', self.trending_image
        yield 'category', self.category
        yield 'htmlShort', self.html_short
        yield 'featured', self.featured
        yield 'date', self.date
        yield 'id', self.id
        yield 'slug', self.slug
        yield 'locale', self.locale
        yield 'categories', self.categories
        yield 'tags', self.tags
        yield 'url', self.url
