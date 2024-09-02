import { Component, computed, inject, signal } from '@angular/core';
import { SaleDataService } from '../../services/data/sale-data.service';
import { toSignal } from '@angular/core/rxjs-interop';
import { NgStyle } from '@angular/common';
import { map } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';

export type SaleVolume = {
    isbn: string;
    display_name: string;
    primary_cover_image_url: string;
    retail_price: number;
    store: string;
    store_price: number;
    is_on_sale: boolean;
    stock_status: string;
    sale_price: number;
    url: string;
};

@Component({
    selector: 'app-browse-sales',
    standalone: true,
    imports: [NgStyle, VolumeCoverTextComponent],
    templateUrl: './browse-sales.component.html',
    styleUrl: './browse-sales.component.css'
})
export class BrowseSalesComponent {

    dialog = inject(MatDialog);

    private readonly _saleDataService = inject(SaleDataService);
    volumes = toSignal(this._saleDataService.saleVolumes$.pipe(
        map(volumes =>
            volumes.map(vol => {
                const bestSale = vol.purchase_options
                    .filter(shopItem => shopItem.is_on_sale)
                    .sort((a, b) => a.store_price - b.store_price)[0];
                return {
                    isbn: vol.isbn,
                    display_name: vol.display_name,
                    primary_cover_image_url: vol.primary_cover_image_url,
                    retail_price: vol.retail_price,
                    ...bestSale,
                    sale_price: Math.round((1 - bestSale.store_price / vol.retail_price) * 100)
                };
            })
        )
    ), { initialValue: [] });

    filterInStock = signal(true);
    filterNoClearance = signal(true);
    filterClearance = signal(false);
    filteredVolumes = computed(() => this.volumes().filter(vol =>
        (vol.stock_status === 'In Stock' || !this.filterInStock())
        && (!this.filterNoClearance() || !this.isCrunchyrollClearance(vol))
        && (!this.filterClearance() || this.isCrunchyrollClearance(vol))
    ));

    isCrunchyrollClearance = (vol: SaleVolume) =>
        vol.store === 'Crunchyroll' &&
        vol.is_on_sale &&
        vol.store_price < vol.retail_price * 0.5;

}
