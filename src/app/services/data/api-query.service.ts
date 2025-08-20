import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { catchError, EMPTY, shareReplay, switchMap } from 'rxjs';

export type Query = {
  order_by?: string;
  limit?: number;
  offset?: number;
};

export type BrowseOptions = {
  status: string[];
  category: string[];
  themes: string[];
  genres: string[];
  authors: string[];
  publishers: string[];
  stores: string[];
  conditions: string[];
  stock_statuses: string[];
  coupons: string[];
};

@Injectable({
  providedIn: 'root'
})
export class APIQueryService {
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _http = inject(HttpClient);

  private readonly OPTIONS_PATH = 'http://localhost:4000/api/browse-options';

  options$ = this._activatedRoute.params.pipe(
    switchMap(() => this._http.get<BrowseOptions>(this.OPTIONS_PATH)),
    shareReplay(),
    catchError(err => {
      console.error('Failed to load options', err);
      return EMPTY;
    })
  );

  parseQuery<T extends Query>(query: T): string {
    return Object.entries(query).reduce(
      (acc, [key, value]) => {
        if (!value && value !== 0) {
          return acc;
        }
        return acc + key + '=' + value + '&';
      },
      (!query.limit ? 'limit=100&' : '') + (!query.offset ? 'offset=0&' : '')
    );
  }
}
