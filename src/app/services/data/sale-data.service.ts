import { Injectable, inject } from '@angular/core';
import { Observable, catchError, EMPTY } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ShopVolume } from '../../interfaces/iShop.interface';
import { APIQueryService } from './api-query.service';

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
