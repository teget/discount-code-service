import json
import uuid

from flask import Flask, request, Response
from services.discount_code_service import DiscountCodeService

app = Flask(__name__)
service = DiscountCodeService()


@app.route("/coupons/<uuid:coupon_id>", methods=['GET'])
def get_coupon(coupon_id):
    """
    Name: Get Coupon
    Desc: Retrieves the coupon with the specified ID, if the coupon is owned by the user accessing the endpoint.
    Endpoint: GET /coupons/<coupon_id>
    Parameters:
        - name: coupon_id
          type: string
          description: The ID for the coupon to be retrieved
    Responses:
        200:
            description: Coupon object to be returned
        404:
            description: Coupon object not found
    """
    customer_id = '59819558-71a0-45fa-b4fe-a030722777b9'  # get real user id from the request (auth improvement)
    coupon = service.get_coupon(customer_id, str(coupon_id))
    if coupon:
        return Response(coupon.to_json(), mimetype='application/json')
    else:
        return Response(json.dumps({'message': 'Coupon not found.'}), mimetype='application/json', status=404)


@app.route("/coupons", methods=['PUT'])
def request_coupon():
    """
    Name: Request coupon
    Desc: Assigns an existing coupon from the specified brand to the calling user and returns it.
    Endpoint: PUT /coupons
    Parameters:
        - name: from_brand
          type: integer
          description: The ID for the brand from which the coupon is requested
    Responses:
        200:
            description: Coupon object that is assigned to the calling user
        400:
            description: Incorrectly formatted brand_id
        404:
            description: Coupon could not be assigned
    """
    from_brand = request.form.get('from_brand')
    try:
        uuid.UUID(from_brand)
    except ValueError:
        return Response(json.dumps({'message': 'brand_id is not a UUID.'}), mimetype='application/json',
                        status=400)

    customer_id = '59819558-71a0-45fa-b4fe-a030722777b9'  # get real user id from the request (auth improvement)
    coupon = service.acquire_coupon(customer_id, from_brand)
    if coupon:
        return Response(coupon.to_json(), mimetype='application/json')
    else:
        return Response(json.dumps({'message': 'Could not assign coupon.'}), mimetype='application/json', status=404)


@app.route("/campaigns", methods=['POST'])
def create_campaign():
    """
    Name: Create campaign
    Desc: Creates a campaign for which a specified number of coupons with a specified amount of discount are created.
    Endpoint: POST /campaigns
    Parameters:
        - name: coupon_ct
          type: integer
          description: The number of coupons to be created for the campaign
        - name: percentage_discount
          type: integer
          description: The percent discount amount for the campaign in
    Responses:
        200:
            description: The newly created campaign object
        400:
            description: Incorrectly formatted parameters
        404:
            description: Campaign could not be created
    """
    coupon_ct = request.form.get('coupon_ct')
    try:
        int(coupon_ct)
    except ValueError:
        return Response(json.dumps({'message': 'coupon_ct is not an integer.'}), mimetype='application/json',
                        status=400)

    percentage_discount = request.form.get('percentage_discount')
    try:
        discount = int(percentage_discount)
        if not 0 < discount <= 100:
            return Response(json.dumps({'message': 'Discount cannot be more than 100 or less than 0.'}),
                            mimetype='application/json', status=400)
    except ValueError:
        return Response(json.dumps({'message': 'coupon_ct is not an integer.'}), mimetype='application/json',
                        status=400)

    for_brand = 'b33f37c1-b731-4826-a7db-d02bdccbe45e'  # get real brand id from the request (auth improvement)
    campaign = service.create_campaign(for_brand, int(coupon_ct), int(percentage_discount))
    if campaign:
        return Response(campaign.to_json(), mimetype='application/json', status=200)
    else:
        return Response(json.dumps({'message': 'Could not create a campaign.'}), mimetype='application/json',
                        status=404)


@app.route("/campaigns/<uuid:campaign_id>/coupons", methods=['GET'])
def get_coupons(campaign_id):
    """
    Name: Get coupons for campaign
    Desc: Retrieves the coupons that are generated for the specified campaign.
    Endpoint: GET /campaigns/<campaign_id>/coupons
    Parameters:
        - name: campaign_id
          type: string
          description: The uuid for the campaign for which the coupons will be retrieved
    Responses:
        200:
            description: A list of coupons that are under the specified campaign
        404:
            description: Coupons not found for the specified campaign
    """
    for_brand = 'b33f37c1-b731-4826-a7db-d02bdccbe45e'  # get real brand id from the request (auth improvement)
    coupons = service.get_campaign_coupons(for_brand, str(campaign_id))
    if coupons:
        return Response([c.to_json() for c in coupons], mimetype='application/json', status=200)
    else:
        return Response(json.dumps({'message': 'No coupons found for the campaign.'}), mimetype='application/json',
                        status=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
