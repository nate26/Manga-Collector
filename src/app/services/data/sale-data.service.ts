import { Injectable, inject } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, map, tap, EMPTY } from 'rxjs';
import { IVolume } from '../../interfaces/iVolume.interface';
import { IGQLGetSaleVolumes } from '../../interfaces/iGQLRequests.interface';
import { UserService } from './user.service';

@Injectable({
    providedIn: 'root'
})
export class SaleDataService {

    private readonly _apollo = inject(Apollo);
    private readonly _userService = inject(UserService);

    private readonly SALE_VOLUMES_QUERY = gql`
        query get_on_sale_volumes($user_id: ID!) {
            get_on_sale_volumes(user_id: $user_id) {
                records {
                    isbn
                    brand
                    series
                    display_name
                    name
                    category
                    volume
                    url
                    release_date
                    publisher
                    format
                    primary_cover_image_url
                    series_data {
                        genres
                        themes {
                            theme
                        }
                    }
                    retail_price
                    purchase_options {
                        store
                        condition
                        url
                        store_price
                        stock_status
                        last_stock_update
                        coupon
                        is_on_sale
                    }
                    user_collection_data {
                        id
                    }
                }
                success
                errors
            }
        }
    `;

    readonly saleVolumes$: Observable<IVolume[]> = this._apollo.watchQuery<IGQLGetSaleVolumes>({
        query: this.SALE_VOLUMES_QUERY,
        variables: { user_id: this._userService.userData().user_id }
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.get_on_sale_volumes.records.slice().sort((a, b) => a.display_name.localeCompare(b.display_name))),
        catchError((err: Error) => {
            console.error('Could not get sale volume data because ', err);
            return EMPTY;
        })
    );

}
