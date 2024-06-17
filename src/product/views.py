from typing import Dict
from decimal import Decimal

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from product.models import ProductModel
from product.serializers import ProductSerializer


class HealthCheck(APIView):
    def get(self, _: Request) -> Response:
        return Response(
            data={"status": "healthy"},
            status=status.HTTP_200_OK,
        )


class Products(APIView):
    def get(self, _: Request) -> Response:
        # get all products
        products = ProductModel.objects.all()
        # serialise the data
        serializer = ProductSerializer(products, many=True)

        # send data
        return Response(
            data={"products": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        # extract request data
        data = request.data
        # serialise data
        serializer = ProductSerializer(data=data)

        try:
            # validate serializer
            serializer.is_valid(raise_exception=True)
            # save product to database
            serializer.save()

            # success response
            return Response(
                data={"product": data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                data={
                    "message": str(e),
                    "data": data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SingleProduct(APIView):
    def get(self, _: Request, product_id: int) -> Response:
        # get product from database
        product = ProductModel.objects.filter(id=product_id).first()

        # if no product found
        if product is None:
            # error response
            return Response(
                data={"message": "invalid 'id' field"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # serialize product
        serializer = ProductSerializer(product)

        # send data
        return Response(
            data={"products": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, product_id: int) -> Response:
        # extract request data
        data: Dict = request.data  # type: ignore

        # get product from database
        product = ProductModel.objects.filter(id=product_id).first()

        # if no product found
        if product is None:
            # error response
            return Response(
                data={
                    "message": "invalid 'id' field",
                    "data": data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "name" in data:
            # assert field type
            assert isinstance(
                data["name"], str
            ), "'name' field should be a string"  # noqa: E501

            # assert field value
            data["name"] = data["name"].strip()
            assert data["name"] != "", "invalid 'name' field"

            # update name field
            product.name = data["name"]

        if "price" in data:
            # assert field type
            assert isinstance(
                data["price"], str
            ), "'price' field should be a decimal"  # noqa: E501

            # cast price to decimal
            data["price"] = Decimal(data["price"])

            # assert field value
            assert data["price"] > Decimal(0.00), "invalid 'price' field"

            # update name field
            product.price = data["price"]

        # save updated product to database
        product.save()
        # serialize product
        serializer = ProductSerializer(product)

        # send updated product
        return Response(
            data={"product": serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, product_id: int) -> Response:
        # extract request data
        data: Dict = request.data  # type: ignore
        # serialise data
        serializer = ProductSerializer(data=data)

        try:
            # validate serializer
            serializer.is_valid(raise_exception=True)
            # get product from database
            product = ProductModel.objects.filter(id=product_id).first()

            # if no product found
            if product is None:
                # error response
                return Response(
                    data={
                        "message": "invalid data",
                        "data": data,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # update & save product
            product.name = data["name"]
            product.price = data["price"]
            product.save()

            # success response
            return Response(
                data={"product": data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                data={
                    "message": str(e),
                    "data": data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, _: Request, product_id: int) -> Response:
        # get product from database
        product = ProductModel.objects.filter(id=product_id).first()

        # if no product found
        if product is None:
            # error response
            return Response(
                data={"message": "invalid 'id' field"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # delete product from database
        product.delete()
        serializer = ProductSerializer(product)

        return Response(
            data={"product": serializer.data},
            status=status.HTTP_200_OK,
        )
