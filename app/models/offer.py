from uuid import uuid4

from app.extensions import db

from .base import GUID, BaseMixin, ModelHelper


class Offer(db.Model, BaseMixin, ModelHelper):
    __tablename__ = 'offers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(GUID(), primary_key=True, default=uuid4)
    alias = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    geo = db.Column(db.String(20), nullable=True)
    img = db.Column(db.Text, nullable=True)
    category_id = db.Column(GUID(), db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=True)
    category = db.relationship('Category')
    description = db.Column(db.Text, nullable=True)
    short_desc = db.Column(db.Text, nullable=True)
    country_code = db.Column(db.String(20), nullable=True)
    payout_share = db.Column(db.Float(), nullable=True, default=0.0)
    ecpc = db.Column(db.Float(), nullable=True, default=0.0)
    price = db.Column(db.Float(), nullable=True, default=0.0)
    meta_data = db.Column(db.JSON(), nullable=True, default=None)
    adv_id = db.Column(GUID(), db.ForeignKey('advs.id', ondelete="CASCADE"), nullable=True)

    @staticmethod
    def from_arguments(args):
        """
            arguments from create offer
            'alias': {'type': 'string'},
            'description': {'type': 'string'},
            'short_desc': {'type': 'string'},
            'geo': {'type': 'string'},
            'name': {'type': 'string'},
            'img': {'type': 'string', 'format': 'uri'},
            'category_id': {'type': 'string', 'format': 'uuid'},
            'country_code': {'type': 'integer'},
            'payout_share': {'type': 'number'},
            'ecpc': {'type': 'number'},
            'price': {'type': 'number'},
            'adv_id': {'type': 'string', 'format': 'uuid'},
            'aff_sub_pub': {'type': 'string'},
            'aff_sub_order': {'type': 'string'},
            'aff_click_id': {'type': 'string'},
            'aff_pub_sub2': {'type': 'string'},
            'account_name':  {'type': 'string'},
            'required': ['name', 'alias', 'description', 'category_id', 'adv_id', 'price', 'img'],
        """
        name = args.get('name')
        alias = args.get('alias')
        geo = args.get('geo', 'global')
        price = args.get('price', 0.0)
        payout_share = args.get('payout_share', 0.0)
        ecpc = args.get('ecpec', 0.0)
        img = args.get('img')
        adv_id = args.get('adv_id')
        category_id = args.get('category_id')
        aff_sub_pub = args.get('aff_sub_pub')
        aff_sub_order = args.get('aff_sub_order')
        aff_click_id = args.get('aff_click_id')
        aff_pub_sub2 = args.get('aff_pub_sub2')
        description = args.get('description')
        short_desc = args.get('short_desc')
        account_name = args.get('account_name')
        meta_data = {'aff_sub_pub': aff_sub_pub, 'aff_sub_order': aff_sub_order,
                     'aff_click_id': aff_click_id, 'aff_pub_sub2': aff_pub_sub2, 'account_name': account_name}
        offer = Offer(
            name=name,
            alias=alias,
            geo=geo,
            price=price,
            payout_share=payout_share,
            ecpc=ecpc,
            img=img,
            adv_id=adv_id,
            category_id=category_id,
            description=description,
            short_desc=short_desc,
            meta_data=meta_data)
        return offer
