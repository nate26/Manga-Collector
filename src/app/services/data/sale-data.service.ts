import { Injectable, inject } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';
import { Observable, catchError, map, tap, EMPTY } from 'rxjs';
import { IGQLGetSaleVolumes } from '../../interfaces/iGQLRequests.interface';
import { UserService } from './user.service';
import { IShopVolume } from '../../interfaces/iShopVolume.interface';

@Injectable({
    providedIn: 'root'
})
export class SaleDataService {

    private readonly _apollo = inject(Apollo);
    private readonly _userService = inject(UserService);

    private readonly SALE_VOLUMES_QUERY = gql`
        query get_on_sale_volumes {
            get_on_sale_volumes {
                records {
                    isbn
                    display_name
                    primary_cover_image_url
                    retail_price
                    store
                    store_price
                    is_on_sale
                    stock_status
                    condition
                    coupon
                    last_stock_update
                    sale_price
                    url
                }
                success
                errors
            }
        }
    `;

    readonly saleVolumes$: Observable<IShopVolume[]> = this._apollo.watchQuery<IGQLGetSaleVolumes>({
        query: this.SALE_VOLUMES_QUERY
    }).valueChanges.pipe(
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.get_on_sale_volumes.records),
        catchError((err: Error) => {
            console.error('Could not get sale volume data because ', err);
            return EMPTY;
        })
    );

}
