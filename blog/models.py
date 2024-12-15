from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.blocks import URLBlock, StructBlock, CharBlock
from wagtail.embeds.blocks import EmbedBlock

class SocialMediaLinksBlock(StructBlock):
    platform = CharBlock(required=True, help_text="Platform name, e.g., YouTube, TikTok, Instagram")
    url = URLBlock(required=True, help_text="Link to the social media content")

    class Meta:
        template = "blog/social_media_links_block.html"

class BlogPage(Page):
    author = models.CharField(max_length=255, help_text="Author or influencer name")
    date = models.DateField("Post date")
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content = StreamField(
        [
            ("heading", CharBlock(form_classname="full title")),
            ("paragraph", RichTextField()),
            ("video", EmbedBlock()),
            ("social_links", StreamField([("social_link", SocialMediaLinksBlock())], blank=True)),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        ImageChooserPanel("header_image"),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Fitness Blog Page"
        verbose_name_plural = "Fitness Blog Pages"