from haystack import indexes
from haystack.sites import site

from faq.models import Topic, Question


class FAQIndexBase(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(stored=True, indexed=False, model_attr='get_absolute_url')


class TopicIndex(FAQIndexBase):
    title = indexes.CharField(model_attr='title', indexed=True)
    site = indexes.CharField(stored=True, faceted=True)

    def prepare(self, object):
        self.prepared_data = super(TopicIndex, self).prepare(object)
        for site in object.sites.all():
            self.prepared_data['site'] = site.name

        return self.prepared_data


    def get_queryset(self):
        return Topic.objects.published()


class QuestionIndex(FAQIndexBase):
    title = indexes.CharField(stored=True, model_attr='question', indexed=True)
    site = indexes.CharField(stored=True, faceted=True)

    def prepare(self, object):
        self.prepared_data = super(QuestionIndex, self).prepare(object)
        for site in object.topic.sites.all():
            self.prepared_data['site'] = site.name

        return self.prepared_data

    def get_queryset(self):
        return Question.objects.published()


site.register(Topic, TopicIndex)
site.register(Question, QuestionIndex)
