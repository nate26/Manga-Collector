import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, tap, map, catchError, throwError, shareReplay } from 'rxjs';
import { IGQLAllRecord, IGQLGetRecord } from '../../interfaces/iGQLRequests.interface';
import { IVolume } from '../../interfaces/iVolume.interface';
import { CollectionDataService } from './collection-data.service';

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
        shareReplay(),
        catchError((err) => throwError(() => new Error('Could not get all volumes because ', err)))
    );

    readonly SINGLE_VOLUME_QUERY = gql`
        query get_record($isbn: ID!, $user_id: ID!) {
            get_record(isbn: $isbn, user_id: $user_id) {
                record {
                    isbn
                    brand
                    series
                    display_name
                    name
                    category
                    volume
                    release_date
                    format
                    pages
                    publisher
                    description
                    primary_cover_image_url
                    series_data {
                        title
                        url
                        description
                        series_match_confidence
                        volumes {
                            isbn
                            volume
                            category
                        }
                        status
                        genres
                        themes {
                            theme
                        }
                    }
                    retail_price
                    user_collection_data {
                        id
                        state
                        cost
                        merchant
                        purchaseDate
                        giftToMe
                        read
                        tags
                        isbn
                        inserted
                        updated
                        user_id
                    }
                }
                success
                errors
            }
        }
    `;

    constructor(private apollo: Apollo, private collectionService: CollectionDataService) { }

    queryVolume(isbn: string): Observable<IVolume> {
        return this.apollo.watchQuery<IGQLGetRecord>({
            query: this.SINGLE_VOLUME_QUERY,
            variables: { isbn, user_id: this.collectionService.USER_ID }
        }).valueChanges.pipe(
            tap(({ error }) => {
                if (error) throw error;
            }),
            map(response => response.data.get_record.record),
            catchError((err) => throwError(() => new Error('Could not get all volumes because ', err)))
        );
    }
}
