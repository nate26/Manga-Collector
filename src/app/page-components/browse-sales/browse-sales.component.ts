import { Component, computed, inject, signal } from '@angular/core';
import { SaleDataService } from '../../services/data/sale-data.service';
import { toSignal } from '@angular/core/rxjs-interop';
import { NgStyle } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';
import { IShopVolume } from '../../interfaces/iShopVolume.interface';

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
    volumes = toSignal(this._saleDataService.saleVolumes$, { initialValue: [] });

    filterInStock = signal(true);
    filterNoClearance = signal(true);
    filterClearance = signal(false);
    filteredVolumes = computed(() => this.volumes().filter(vol =>
        (vol.stock_status === 'In Stock' || !this.filterInStock())
        && (!this.filterNoClearance() || !this.isCrunchyrollClearance(vol))
        && (!this.filterClearance() || this.isCrunchyrollClearance(vol))
    ));

    isCrunchyrollClearance = (vol: IShopVolume) =>
        vol.store === 'Crunchyroll' &&
        vol.is_on_sale &&
        vol.store_price < vol.retail_price * 0.5;

}
