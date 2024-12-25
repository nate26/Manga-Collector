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
}

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
};

export type SeriesQuery = Query & {
    title?: string;
    // ...
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
            console.error(
                'Could not get all series data because ',
                err
            );
            return EMPTY;
        })
    );

    series = pipe(
        map(series_id => this.SERIES_PATH + '/' + series_id),
        switchMap(url => this._http.get<SeriesOutput>(url)),
        catchError((err: Error) => {
            console.error(
                'Could not get series data because ',
                err
            );
            return EMPTY;
        })
    );
}
