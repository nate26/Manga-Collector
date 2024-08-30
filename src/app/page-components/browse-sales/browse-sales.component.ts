import { Component, inject } from '@angular/core';
import { SaleDataService } from '../../services/data/sale-data.service';
import { toSignal } from '@angular/core/rxjs-interop';
import { NgStyle } from '@angular/common';

@Component({
    selector: 'app-browse-sales',
    standalone: true,
    imports: [NgStyle],
    templateUrl: './browse-sales.component.html',
    styleUrl: './browse-sales.component.css'
})
export class BrowseSalesComponent {

    private readonly _saleDataService = inject(SaleDataService);
    volumes = toSignal(this._saleDataService.saleVolumes$, { initialValue: [] });

}
