import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import { Observable, catchError, map, tap, throwError } from 'rxjs';
import { IManga } from '../interfaces/iManga.interface';
import { GET_MANGA } from '../graphql-operations';
import { IGQLListMangaRecords } from '../interfaces/iGraphQLRequests.interface';

@Injectable({
    providedIn: 'root'
})
export class MangaRecordService {

    readonly listMangaRecords$: Observable<IManga[]> = this.apollo.watchQuery<IGQLListMangaRecords>({
        query: GET_MANGA,
        variables: { user_id: '', isbn: '9781947194779' }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.list_manga_records.manga_records),
        catchError(() => throwError(() => new Error('Could not get data')))
    );

    constructor(private apollo: Apollo) { }

}
