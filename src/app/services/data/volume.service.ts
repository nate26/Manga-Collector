import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, tap, map, catchError, throwError } from 'rxjs';
import { IGQLAllRecord } from '../../interfaces/iGQLRequests.interface';
import { IVolume } from '../../interfaces/iVolume.interface';

@Injectable({
    providedIn: 'root'
})
export class VolumeService {

    readonly VOLUMES_BASIC_QUERY = gql`
        query all_records($user_id: ID) {
            all_records(user_id: $user_id) {
                records {
                    isbn
                    series
                    display_name
                    volume
                    primary_cover_image_url
                }
                success
                errors
            }
        }
    `;

    volumesBasic$: Observable<IVolume[]> = this.apollo.watchQuery<IGQLAllRecord>({
        query: this.VOLUMES_BASIC_QUERY,
        variables: { user_id: null }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.all_records.records),
        catchError((err) => throwError(() => new Error('Could not get all volumes because ', err)))
    );

    constructor(private apollo: Apollo) { }
}
