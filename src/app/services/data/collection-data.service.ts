import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, filter, map, switchMap, tap, throwError } from 'rxjs';
import { IVolume } from '../../interfaces/iVolume.interface';
import { IGQLGetCollectionVolumes } from '../../interfaces/iGQLRequests.interface';
import { HttpClient } from '@angular/common/http';
import { ICollection } from '../../interfaces/iCollection.interface';

@Injectable({
    providedIn: 'root'
})
export class CollectionDataService {
    private serviceURL = '';

    readonly COLLECTION_VOLUMES_QUERY = gql`
        query get_collection_volumes($user_id: ID!) {
            get_collection_volumes(user_id: $user_id) {
                records {
                    isbn
                    brand
                    series
                    display_name
                    name
                    category
                    volume
                    release_date
                    publisher
                    primary_cover_image_url
                    series_data {
                        title
                        url
                        series_match_confidence
                        volumes {
                            isbn
                            volume
                            category
                        }
                        status
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

    collectionVolumes$: Observable<IVolume[]> = this.apollo.watchQuery<IGQLGetCollectionVolumes>({
        query: this.COLLECTION_VOLUMES_QUERY,
        variables: { user_id: 'f69c759a-00dd-4dbe-8e58-96cd7a05969e' }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.get_collection_volumes.records.map(vol => ({
            ...vol,
            user_collection_data: vol.user_collection_data.map(collection => ({
                ...collection,
                tags: collection.tags ?? []
            }))
        }))),
        catchError((err) => throwError(() => new Error('Could not get data because ' + err)))
    );

    saveToCollection = (source$: Observable<ICollection[]>) => source$.pipe(
        filter(records => records.length > 0),
        switchMap(records => this.http.post(`${this.serviceURL}/add-records`, records))
    );

    constructor(private apollo: Apollo, private http: HttpClient) { }

}
