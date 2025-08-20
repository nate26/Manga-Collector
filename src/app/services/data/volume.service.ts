import { Injectable, inject } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, tap, map, catchError, throwError, shareReplay, switchMap, of } from 'rxjs';
import { IGQLAllRecord, IGQLGetRecord } from '../../interfaces/iGQLRequests.interface';
import { IVolume } from '../../interfaces/iVolume.interface';
import { UserService } from './user.service';

@Injectable({
    providedIn: 'root'
})
export class VolumeService {

    private readonly apollo = inject(Apollo);
    private readonly userService = inject(UserService);

    private readonly VOLUMES_BASIC_QUERY = gql`
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

    readonly volumesBasic$: Observable<IVolume[]> = this.apollo.watchQuery<IGQLAllRecord>({
        query: this.VOLUMES_BASIC_QUERY,
        variables: { user_id: null }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.all_records.records),
        shareReplay(),
        catchError((err) =>
            throwError(() =>
                Error('Could not get all volumes because ' + err.message, err)
            )
        )
    );

    private readonly SINGLE_VOLUME_QUERY = gql`
        query get_record($isbn: ID!, $user_id: ID!) {
            get_record(isbn: $isbn, user_id: $user_id) {
                record {
                    isbn
                    brand
                    series
                    series_id
                    display_name
                    name
                    category
                    volume
                    url
                    record_added_date
                    record_updated_date
                    release_date
                    publisher
                    format
                    pages
                    authors
                    isbn_10
                    primary_cover_image_url
                    other_images {
                        name
                        url
                    }
                    description
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

    queryVolume(isbn: string): Observable<IVolume> {
        return of(this.userService.userData()).pipe(
            switchMap(({ user_id }) =>
                this.apollo.watchQuery<IGQLGetRecord>(
                    { query: this.SINGLE_VOLUME_QUERY, variables: { isbn, user_id } }
                ).valueChanges
            ),
            tap(({ error }) => {
                if (error) throw error;
            }),
            map(response => response.data.get_record.record!),
            catchError((err) =>
                throwError(() =>
                    new Error('Could not get all volumes because ' + err.message, err)
                )
            )
        );
    }
}
