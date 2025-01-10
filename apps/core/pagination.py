# -----------------------------------------------------------------------------
# Copyright (c) 2025 Tekyonix
# All rights reserved.
#
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# -----------------------------------------------------------------------------

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginationWithCount(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination to include
    additional pagination details and support for sorting based on user input.
    """

    page_size = 10
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate the queryset with custom sorting based on the 'ordering' query parameter.
        """
        # Get the ordering parameter from the request, default to '-created_at' if not provided
        ordering = request.query_params.get('ordering', 'created_at')
        # Split the ordering parameter to handle multiple fields
        ordering_fields = ordering.split(',')
        # Apply custom sorting
        queryset = queryset.order_by(*ordering_fields)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """
        Return a paginated response with additional pagination details.
        """
        return Response(
            {
                'page_size': self.page_size,
                'total_objects': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page_number': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        )
