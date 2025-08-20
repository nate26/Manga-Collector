import { Injectable, inject } from '@angular/core';
import { EMPTY, catchError, debounceTime, map, pipe, switchMap } from 'rxjs';
import { APIQueryService, Query } from './api-query.service';
import { HttpClient } from '@angular/common/http';

export type SeriesVolume = {
  isbn: string;
  name: string;
  volume: string;
  category: string;
  stock_status: string;
  release_date: string;
  primary_cover_image: string;
  format: string;
};

type Theme = {
  theme: string;
  votes: number;
};

export type SeriesDetails = {
  name: string;
  type: string;
};

export type SeriesOutput = {
  title: string;
  cover_image: string;
  category: string;
  status: string;
  url: string;
  series_id: string;
  volumes: SeriesVolume[];
  genres: string[];
  themes: Theme[];
  description: string;
  release_status: string;
  latest_chapter: number;
  authors: SeriesDetails[];
  publishers: SeriesDetails[];
  bayesian_rating: number;
  rank: number;
  recommendations: number[];
};

export type SeriesQuery = Query & {
  title?: string;
  status?: string;
  category?: string;
  genre?: string;
  theme?: string;
  author?: string;
  publisher?: string;
  rank_le?: number;
  rank_ge?: number;
  rating_le?: number;
  rating_ge?: number;
};

@Injectable({
  providedIn: 'root'
})
export class SeriesDataService {
  private readonly _http = inject(HttpClient);
  private readonly _queryService = inject(APIQueryService);

  private readonly SERIES_PATH = 'http://localhost:4000/api/series';

  seriesSearch = pipe(
    map((query: SeriesQuery) => this.SERIES_PATH + '?' + this._queryService.parseQuery(query)),
    debounceTime(300),
    switchMap(url => this._http.get<SeriesOutput[]>(url)),
    catchError((err: Error) => {
      console.error('Could not get all series data because ', err);
      return EMPTY;
    })
  );

  getSeries(series_id: number) {
    const url = this.SERIES_PATH + '/' + series_id;
    return this._http.get<SeriesOutput>(url).pipe(
      catchError((err: Error) => {
        console.error('Could not get series data because ', err);
        return EMPTY;
      })
    );
  }
}
