from flask_restful import Resource
from flask import request, redirect
from api_service.extensions import db
from api_service.models import Url as UrlModel
from typing import Optional


class UrlShortner(Resource):
    """
    API endpoint responsible for url shortner
    """

    def post(self):
        """Here is were we get the url request to short"""
        url: Optional[str] = request.json.get("url")
        if not url:
            {"bad_request": "url not found in the request"}, 400
        url_exists = UrlModel.query.filter_by(long_url=url).first()

        if url_exists:
            # increase count
            url_exists.count += 1
            db.session.add(url_exists)
            db.session.commit()
            return {"short_url": url_exists.short_url}

        url_model = UrlModel(long_url=url, count=1)
        db.session.add(url_model)
        db.session.commit()

        short_code = self.shorten(url_model.id)
        short_url = f"http://localhost:5000/{short_code}"

        url_model.short_code = short_code
        url_model.short_url = short_url
        db.session.commit()

        return {"short_url": short_url}

    def shorten(self, num: int) -> str:
        """
        Convert an integer to a short URL code with base 62
        """
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(alphabet)
        result = []
        while num > 0:
            num, remainder = divmod(num, base)
            result.append(alphabet[remainder])
        return "".join(reversed(result))

    def delete(self):
        """Here is were delete a url"""
        id: int = request.args.get("id", None)
        print(id)
        if not id:
            {"bad_request": "need id to delete"}, 400

        url_value = UrlModel.query.get(id)
        if not url_value:
            return {"not_found": "doesnt exist"}, 404
        db.session.delete(url_value)
        db.session.commit()

        return {"message": "Deleted"}, 200


class RedirectURL(Resource):
    def get(self, short_code):
        url_exists = UrlModel.query.filter_by(short_code=short_code).first()
        if url_exists:
            return redirect(url_exists.long_url)
        else:
            return {"error": "Short URL not found"}, 404


class UrlStats(Resource):
    def get(self):
        top_urls = (
            db.session.query(UrlModel.long_url, UrlModel.count)
            .order_by(db.desc(UrlModel.count))
            .limit(100)
            .all()
        )

        if not top_urls:
            return [], 200

        top_urls_list = [{"long_url": url, "count": count} for url, count in top_urls]
        return {"top_urls": top_urls_list}
