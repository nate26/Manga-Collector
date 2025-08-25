import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { EMPTY, Observable, catchError } from 'rxjs';
import { APIQueryService } from './api-query.service';

export type Shop = {
  item_id: string;
  isbn: string;
  store: string;
  url: string;
  condition: string;
  price: number;
  stock_status: string;
  last_stock_update: string;
  coupon: string;
  is_on_sale: boolean;
  promotion: string;
  promotion_percentage: number;
  backorder_details: string;
  exclusive: boolean;
  is_bundle: boolean;
};

export type ShopVolume = Shop & {
  volume: {
    name: string;
    display_name: string;
    category: string;
    volume: string;
    brand: string;
    series: string;
    series_id: string;
    edition: string;
    edition_id: string;
    release_date: string;
    primary_cover_image: string;
  };
  market: {
    retail_price: number;
  };
};

export type ShopQuery = {
  order_by?: string;
  limit?: number;
  offset?: number;
  store?: string;
  condition?: string;
  stock?: string;
  promo?: string;
  on_sale?: boolean;
  exclusive?: boolean;
  bundle?: boolean;
  price?: number;
  price_lt?: number;
  price_le?: number;
  price_gt?: number;
  price_ge?: number;
  promo_perc?: number;
  promo_perc_lt?: number;
  promo_perc_le?: number;
  promo_perc_gt?: number;
  promo_perc_ge?: number;
};

@Injectable({
  providedIn: 'root'
})
export class SaleDataService {
  private readonly _http = inject(HttpClient);
  private readonly _queryService = inject(APIQueryService);

  getSaleVolumes$(query: ShopQuery): Observable<ShopVolume[]> {
    return this._http
      .get<ShopVolume[]>('http://localhost:4000/api/shop?' + this._queryService.parseQuery(query))
      .pipe(
        catchError((err: Error) => {
          console.error('Could not get sale volume data because ', err);
          return EMPTY;
        })
      );
  }
}
