import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, map, tap, throwError } from 'rxjs';
import { IVolume } from '../../interfaces/iVolume.interface';
import { IGQLGetCollectionVolumes } from '../../interfaces/iGQLRequests.interface';

@Injectable({
    providedIn: 'root'
})
export class CollectionDataService {

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
                        volumes {
                            isbn
                            volume
                            category
                        }
                        status
                    }
                    retail_price
                    user_collection_data {
                        state
                        cost
                        merchant
                        purchaseDate
                        giftToMe
                        read
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
        map(response => response.data.get_collection_volumes.records),
        catchError((err) => throwError(() => new Error('Could not get data because ' + err)))
    );

    constructor(private apollo: Apollo) { }

}
