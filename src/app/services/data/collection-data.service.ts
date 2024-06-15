import { Injectable } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, map, of, tap, throwError } from 'rxjs';
import { IVolume } from '../../interfaces/iVolume.interface';
import { IGQLDeleteCollectionResult, IGQLGetCollectionVolumes, IGQLModifyCollectionResult } from '../../interfaces/iGQLRequests.interface';
import { ICollection } from '../../interfaces/iCollection.interface';

@Injectable({
    providedIn: 'root'
})
export class CollectionDataService {
    public USER_ID = 'f69c759a-00dd-4dbe-8e58-96cd7a05969e';

    readonly COLLECTION_VOLUMES_QUERY = gql`
        query get_collection_volumes($user_id: ID!) {
            get_collection_volumes(user_id: $user_id) {
                records {
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

    collectionVolumes$: Observable<IVolume[]> = this.apollo.watchQuery<IGQLGetCollectionVolumes>({
        query: this.COLLECTION_VOLUMES_QUERY,
        variables: { user_id: this.USER_ID }
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
        catchError((err: Error) => throwError(() => 'Could not get data because ' + err.message))
    );

    readonly MODIFY_COLLECTION = gql`
        mutation modify_collection($user_id: ID!, $volumes_update: [CollectionDataInput]!) {
            modify_collection(user_id: $user_id, volumes_update: $volumes_update) {
                response {
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
                success
                errors
            }
        }
    `;

    readonly DELETE_COLLECTION = gql`
    mutation delete_collection_records($user_id: ID!, $ids_delete: [String]!) {
        delete_collection_records(user_id: $user_id, ids_delete: $ids_delete) {
            response
            success
            errors
        }
    }
`;

    constructor(private apollo: Apollo) { }

    saveToCollection(records: ICollection[]) {
        if (records.length === 0) return of([]);
        return this.apollo.mutate<IGQLModifyCollectionResult>({
            mutation: this.MODIFY_COLLECTION,
            variables: { user_id: this.USER_ID, volumes_update: records }
        }).pipe(
            map(result => {
                if (result.data?.modify_collection.success && result.data?.modify_collection.response) {
                    return result.data.modify_collection.response
                }
                else {
                    console.error('could not save data... ', result)
                    throw new Error(result.errors?.join(', '));
                }
            }),
            catchError((err: Error) => throwError(() => 'Could not save data because ' + err.message))
        );
    }

    deleteFromCollection(records: string[]) {
        if (records.length === 0) return of([]);
        return this.apollo.mutate<IGQLDeleteCollectionResult>({
            mutation: this.DELETE_COLLECTION,
            variables: { user_id: this.USER_ID, ids_delete: records }
        }).pipe(
            map(result => {
                if (result.data?.delete_collection_records.success && result.data?.delete_collection_records.response) {
                    return result.data.delete_collection_records.response
                }
                else {
                    console.error('could not delete data... ', result)
                    throw new Error(result.errors?.join(', '));
                }
            }),
            catchError((err: Error) => throwError(() => 'Could not delete data because ' + err.message))
        );
    }

    buildNewRecord(vol: IVolume): ICollection {
        return {
            isbn: vol.isbn,
            state: '',
            cost: 0,
            merchant: '',
            purchaseDate: '',
            giftToMe: false,
            read: false,
            tags: [],
            user_id: this.USER_ID,
            temp_id: Date.now().toString()
        }
    }

}
