import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, map, tap, throwError } from 'rxjs';
import { ISeriesRecord } from '../../interfaces/iSeries.interface';
import { IGQLGetCollectionSeries } from '../../interfaces/iGQLRequests.interface';

@Injectable({
    providedIn: 'root'
})
export class SeriesDataService {
    public USER_ID = 'f69c759a-00dd-4dbe-8e58-96cd7a05969e';

    readonly SERIES_VOLUMES_QUERY = gql`
        query get_collection_series($user_id: ID!) {
            get_collection_series(user_id: $user_id) {
                records {
                    series_id
                    title
                    associated_titles
                    url
                    category
                    series_match_confidence
                    description
                    cover_image
                    genres
                    themes {
                        theme
                    }
                    latest_chapter
                    release_status
                    status
                    authors {
                        name
                        type
                    }
                    publishers {
                        name
                        type
                    }
                    bayesian_rating
                    rank
                    recommendations
                    volumes {
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
                        retail_price
                        user_collection_data {
                            id
                        }
                    }
                }
                success
                errors
            }
        }
    `;

    collectionSeries$: Observable<ISeriesRecord[]> = this.apollo.watchQuery<IGQLGetCollectionSeries>({
        query: this.SERIES_VOLUMES_QUERY,
        variables: { user_id: this.USER_ID }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.get_collection_series.records.map(series => ({
            ...series,
            volumes: series.volumes.map(vol => ({
                ...vol,
                // this should probably be handled in the backend
                user_collection_data: (vol.user_collection_data ?? []).map(collection => ({
                    ...collection,
                    tags: collection.tags ?? []
                }))
            }))
        }))),
        catchError((err: Error) => throwError(() => 'Could not get data because ' + err.message))
    );

    constructor(private apollo: Apollo) { }

}
