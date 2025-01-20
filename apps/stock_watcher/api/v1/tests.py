from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.stock_watcher.tests.factories.watchlist_factory import (
    WatchlistFactory,
    WatchlistStockFactory,
)
from apps.users.tests.factories.custom_user import CustomUserFactory


class WatchlistBaseAPITest(APITestCase):
    def setUp(self):
        self.watchlists = []
        self.user = CustomUserFactory()
        self.client.force_authenticate(user=self.user)

    def generate_data(self, user=None):
        if not user:
            user = self.user
        self.watchlists.append(WatchlistFactory(user=user))

    def add_stock_to_watchlist(self, watchlist):
        # Add stock to watchlist
        stock = WatchlistStockFactory(watchlist=watchlist)
        return stock


class WatchlistGetAPITest(WatchlistBaseAPITest):
    maxDiff = None

    def test_empty_watchlist(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 0)

    def test_get_stock_watchlist(self):
        self.generate_data()
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [],
            },
        )

    def test_multiple_watchlists(self):
        self.generate_data()
        self.generate_data()
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 2)

    def test_watchlist_with_single_stock(self):
        self.generate_data()
        self.add_stock_to_watchlist(self.watchlists[0])

        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    1,
                ],
            },
        )

    def test_watchlist_with_multiple_stocks(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.add_stock_to_watchlist(watchlist)
        self.add_stock_to_watchlist(watchlist)

        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    1,
                    2,
                ],
            },
        )

    def test_get_watchlist_when_multiple_users(self):
        self.generate_data()
        user2 = CustomUserFactory()
        self.generate_data(user2)
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [],
            },
        )

    def test_get_stock_watchlist_when_invalid_user(self):
        self.generate_data()
        user2 = CustomUserFactory()
        self.client.force_authenticate(user=user2)
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 0)

    def test_get_stock_watchlist_when_multiple_users(self):
        self.generate_data()
        self.add_stock_to_watchlist(self.watchlists[0])
        user2 = CustomUserFactory()
        self.generate_data(user2)
        self.add_stock_to_watchlist(self.watchlists[1])
        self.add_stock_to_watchlist(self.watchlists[1])
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    1,
                ],
            },
        )


class WatchlistDetailAPITest(WatchlistBaseAPITest):
    def test_watchlist_detail_with_single_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)

        response = self.client.get(reverse('watchlist-detail', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': watchlist.id,
                'name': watchlist.name,
                'currency': watchlist.currency,
                'created_at': watchlist.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    {
                        'id': stock.id,
                        'symbol': stock.symbol,
                        'name': stock.name,
                        'current_price': str(stock.current_price),
                        'added_price': str(stock.added_price),
                        'pe_ratio': str(stock.pe_ratio),
                        'suggestion': stock.suggestion,
                        'created_at': stock.created_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                        'updated_at': stock.updated_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                    }
                ],
            },
        )

    def test_watchlist_detail_with_multiple_stocks(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock1 = self.add_stock_to_watchlist(watchlist)
        stock2 = self.add_stock_to_watchlist(watchlist)

        response = self.client.get(reverse('watchlist-detail', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data,
            {
                'id': watchlist.id,
                'name': watchlist.name,
                'currency': watchlist.currency,
                'created_at': watchlist.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    {
                        'id': stock1.id,
                        'symbol': stock1.symbol,
                        'name': stock1.name,
                        'current_price': str(stock1.current_price),
                        'added_price': str(stock1.added_price),
                        'pe_ratio': str(stock1.pe_ratio),
                        'suggestion': stock1.suggestion,
                        'created_at': stock1.created_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                        'updated_at': stock1.updated_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                    },
                    {
                        'id': stock2.id,
                        'symbol': stock2.symbol,
                        'name': stock2.name,
                        'current_price': str(stock2.current_price),
                        'added_price': str(stock2.added_price),
                        'pe_ratio': str(stock2.pe_ratio),
                        'suggestion': stock2.suggestion,
                        'created_at': stock2.created_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                        'updated_at': stock2.updated_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                    },
                ],
            },
        )

    def test_get_watchlist_detail_when_multiple_users(self):
        self.generate_data()
        user2 = CustomUserFactory()
        self.generate_data(user2)
        response = self.client.get(
            reverse('watchlist-detail', args=[self.watchlists[0].id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reference = self.watchlists[0]
        self.assertDictEqual(
            response.data,
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [],
            },
        )

    def test_get_watchlist_detail_when_invalid_watchlist(self):
        self.generate_data()
        response = self.client.get(reverse('watchlist-detail', args=[100]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_stock_watchlist_detail_when_multiple_users(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.add_stock_to_watchlist(watchlist)
        user2 = CustomUserFactory()
        self.generate_data(user2)
        watchlist = self.watchlists[1]
        stock1 = self.add_stock_to_watchlist(watchlist)
        stock2 = self.add_stock_to_watchlist(watchlist)
        response = self.client.get(reverse('watchlist-detail', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reference = self.watchlists[1]
        self.assertDictEqual(
            response.data,
            {
                'id': reference.id,
                'name': reference.name,
                'currency': reference.currency,
                'created_at': reference.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'stocks': [
                    {
                        'id': stock1.id,
                        'symbol': stock1.symbol,
                        'name': stock1.name,
                        'current_price': str(stock1.current_price),
                        'added_price': str(stock1.added_price),
                        'pe_ratio': str(stock1.pe_ratio),
                        'suggestion': stock1.suggestion,
                        'created_at': stock1.created_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                        'updated_at': stock1.updated_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                    },
                    {
                        'id': stock2.id,
                        'symbol': stock2.symbol,
                        'name': stock2.name,
                        'current_price': str(stock2.current_price),
                        'added_price': str(stock2.added_price),
                        'pe_ratio': str(stock2.pe_ratio),
                        'suggestion': stock2.suggestion,
                        'created_at': stock2.created_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                        'updated_at': stock2.updated_at.strftime(
                            '%Y-%m-%dT%H:%M:%S.%fZ'
                        ),
                    },
                ],
            },
        )


class WatchlistCreateAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_watchlist(self):
        data = {
            'name': 'Test Watchlist',
            'currency': 1,
        }
        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Watchlist')
        self.assertEqual(response.data['currency'], 1)
        self.assertEqual(response.data['stocks'], [])

    def test_create_watchlist_with_invalid_currency(self):
        data = {
            'name': 'Test Watchlist',
            'currency': 100,
        }
        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_watchlist_with_invalid_name(self):
        data = {
            'name': '',
            'currency': 1,
        }
        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_watchlist_with_duplicate_name(self):
        WatchlistFactory(user=self.user, name='Test Watchlist')
        data = {
            'name': 'Test Watchlist',
            'currency': 1,
        }
        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_watchlist_with_no_user(self):
        self.client.force_authenticate(user=None)
        data = {
            'name': 'Test Watchlist',
            'currency': 1,
        }
        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WatchlistUpdateAPITest(WatchlistBaseAPITest):
    def test_update_watchlist(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        data = {
            'name': watchlist.name,
            'currency': 2,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], watchlist.name)
        self.assertEqual(response.data['currency'], 2)

    def test_update_watchlist_name(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        data = {
            'name': 'Updated Name',
            'currency': watchlist.currency,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['currency'], watchlist.currency)

    def test_update_watchlist_with_invalid_currency(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        data = {
            'currency': 100,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_watchlist_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.client.force_authenticate(user=None)
        data = {
            'currency': 1,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_watchlist_with_invalid_watchlist(self):
        self.generate_data()
        data = {
            'currency': 1,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[100]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_when_stocks_are_present(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        data = {
            'name': watchlist.name,
            'currency': 2,
        }
        response = self.client.put(
            reverse('watchlist-detail', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency'], 2)
        self.assertEqual(
            response.data['stocks'],
            [
                {
                    'id': stock.id,
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'current_price': str(stock.current_price),
                    'added_price': str(stock.added_price),
                    'pe_ratio': str(stock.pe_ratio),
                    'suggestion': stock.suggestion,
                    'created_at': stock.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    'updated_at': stock.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                }
            ],
        )


class WatchlistDeleteAPITest(WatchlistBaseAPITest):
    def test_delete_watchlist(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        response = self.client.delete(
            reverse('watchlist-detail', args=[watchlist.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_watchlist_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse('watchlist-detail', args=[watchlist.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_watchlist_with_invalid_watchlist(self):
        self.generate_data()
        response = self.client.delete(reverse('watchlist-detail', args=[100]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_watchlist_with_stocks(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.add_stock_to_watchlist(watchlist)
        response = self.client.delete(
            reverse('watchlist-detail', args=[watchlist.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(len(watchlist.stocks.all()), 0)


class WatchlistStockGetAPITest(WatchlistBaseAPITest):
    def test_get_watchlist_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        response = self.client.get(reverse('watchlist-stocks', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': str(stock.current_price),
                'added_price': str(stock.added_price),
                'pe_ratio': str(stock.pe_ratio),
                'suggestion': stock.suggestion,
                'created_at': stock.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': stock.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

    def test_get_watchlist_stock_with_multiple_stocks(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock1 = self.add_stock_to_watchlist(watchlist)
        stock2 = self.add_stock_to_watchlist(watchlist)
        response = self.client.get(reverse('watchlist-stocks', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 2)
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': stock1.id,
                'symbol': stock1.symbol,
                'name': stock1.name,
                'current_price': str(stock1.current_price),
                'added_price': str(stock1.added_price),
                'pe_ratio': str(stock1.pe_ratio),
                'suggestion': stock1.suggestion,
                'created_at': stock1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': stock1.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )
        self.assertDictEqual(
            response.data['results'][1],
            {
                'id': stock2.id,
                'symbol': stock2.symbol,
                'name': stock2.name,
                'current_price': str(stock2.current_price),
                'added_price': str(stock2.added_price),
                'pe_ratio': str(stock2.pe_ratio),
                'suggestion': stock2.suggestion,
                'created_at': stock2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': stock2.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

    def test_get_watchlist_stock_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('watchlist-stocks', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_watchlist_stock_with_invalid_watchlist(self):
        self.generate_data()
        response = self.client.get(reverse('watchlist-stocks', args=[100]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 0)

    def test_get_watchlist_stock_when_multiple_users(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        user2 = CustomUserFactory()
        self.generate_data(user2)
        response = self.client.get(reverse('watchlist-stocks', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': str(stock.current_price),
                'added_price': str(stock.added_price),
                'pe_ratio': str(stock.pe_ratio),
                'suggestion': stock.suggestion,
                'created_at': stock.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': stock.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )

    def test_get_watchlist_stock_when_multiple_watchlist(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        self.generate_data()
        watchlist2 = self.watchlists[1]
        stock2 = self.add_stock_to_watchlist(watchlist2)
        response = self.client.get(reverse('watchlist-stocks', args=[watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_objects'], 1)
        self.assertDictEqual(
            response.data['results'][0],
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': str(stock.current_price),
                'added_price': str(stock.added_price),
                'pe_ratio': str(stock.pe_ratio),
                'suggestion': stock.suggestion,
                'created_at': stock.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'updated_at': stock.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            },
        )


class WatchlistStockCreateAPITest(WatchlistBaseAPITest):
    def test_create_watchlist_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.post(
            reverse('watchlist-stocks', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['symbol'], 'AAPL')
        self.assertEqual(response.data['name'], 'Apple Inc')
        self.assertEqual(response.data['added_price'], '100.00')
        self.assertEqual(response.data['current_price'], '0.00')
        self.assertEqual(response.data['pe_ratio'], '0.00')
        self.assertEqual(response.data['suggestion'], 0)

    def test_create_watchlist_stock_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        self.client.force_authenticate(user=None)
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.post(
            reverse('watchlist-stocks', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_watchlist_stock_with_invalid_watchlist(self):
        self.generate_data()
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.post(
            reverse('watchlist-stocks', args=[100]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_watchlist_stock_with_invalid_data(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
        }
        response = self.client.post(
            reverse('watchlist-stocks', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_watchlist_stock_with_invalid_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        user2 = CustomUserFactory()
        self.client.force_authenticate(user=user2)
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.post(
            reverse('watchlist-stocks', args=[watchlist.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WatchlistStockUpdateAPITest(WatchlistBaseAPITest):
    def test_update_watchlist_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.put(
            reverse('watchlist-stock-detail', args=[watchlist.id, stock.id]),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'AAPL')
        self.assertEqual(response.data['name'], 'Apple Inc')
        self.assertEqual(response.data['added_price'], '100.00')
        self.assertEqual(response.data['current_price'], str(stock.current_price))
        self.assertEqual(response.data['pe_ratio'], str(stock.pe_ratio))
        self.assertEqual(response.data['suggestion'], stock.suggestion)

    def test_update_watchlist_stock_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        self.client.force_authenticate(user=None)
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.put(
            reverse('watchlist-stock-detail', args=[watchlist.id, stock.id]),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_watchlist_stock_with_invalid_watchlist(self):
        self.generate_data()
        stock = WatchlistStockFactory()
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.put(
            reverse('watchlist-stock-detail', args=[100, stock.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_watchlist_stock_with_invalid_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc',
            'added_price': 100,
        }
        response = self.client.put(
            reverse('watchlist-stock-detail', args=[watchlist.id, 100]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WatchlistStockDeleteAPITest(WatchlistBaseAPITest):
    def test_delete_watchlist_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        response = self.client.delete(
            reverse('watchlist-stock-detail', args=[watchlist.id, stock.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_watchlist_stock_with_no_user(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse('watchlist-stock-detail', args=[watchlist.id, stock.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_watchlist_stock_with_invalid_watchlist(self):
        self.generate_data()
        stock = WatchlistStockFactory()
        response = self.client.delete(
            reverse('watchlist-stock-detail', args=[100, stock.id])
        )
        # TODO(gobind): Should be 400 instead of 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_watchlist_stock_with_invalid_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        stock = self.add_stock_to_watchlist(watchlist)
        response = self.client.delete(
            reverse('watchlist-stock-detail', args=[watchlist.id, 100])
        )
        # TODO(gobind): Should be 400 instead of 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_watchlist_stock_with_no_stock(self):
        self.generate_data()
        watchlist = self.watchlists[0]
        response = self.client.delete(
            reverse('watchlist-stock-detail', args=[watchlist.id, 100])
        )
        # TODO(gobind): Should be 400 instead of 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
