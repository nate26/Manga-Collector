import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import { Observable, catchError, map, tap, throwError } from 'rxjs';
import { GET_MANGA } from '../graphql-operations';
import { IVolume } from '../interfaces/iVolume.interface';
import { IGQLGetCollectionVolumes } from '../interfaces/iGQLRequests.interface';

@Injectable({
    providedIn: 'root'
})
export class MangaRecordService {

    readonly listMangaRecords$: Observable<IVolume[]> = this.apollo.watchQuery<IGQLGetCollectionVolumes>({
        query: GET_MANGA,
        variables: { user_id: '', isbn: '9781947194779' }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.get_collection_volumes.get_collection_volumes),
        catchError(() => throwError(() => new Error('Could not get data')))
    );

    constructor(private apollo: Apollo) { }

}
