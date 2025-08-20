import { CommonModule } from '@angular/common';
import { Component, EventEmitter } from '@angular/core';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { CollectionService } from '../../services/collection.service';
import { trigger, transition, style, animate } from '@angular/animations';
import { FormsModule } from '@angular/forms';
import { IVolume } from '../../interfaces/iVolume.interface';

@Component({
    selector: 'app-list-view',
    standalone: true,
    imports: [CommonModule, FormsModule, MatCheckboxModule],
    templateUrl: './list-view.component.html',
    styleUrl: './list-view.component.css',
    animations: [
        trigger('fade', [
            transition('false => true', [
                style({ opacity: 0 }),
                animate(400, style({ opacity: 1 }))
            ]),
            transition('true => false', [
                style({ opacity: 1 }),
                animate(400, style({ opacity: 0 }))
            ])
        ])
    ]
})
export class ListViewComponent {

    protected readonly volumes$ = this.collectionService.collectionAsVolume$;

    // put edit in service smh
    editVolume = new EventEmitter<IVolume>();

    constructor(private collectionService: CollectionService) { }

    edit(vol: IVolume) {
        this.editVolume.emit(vol)
    }

    getStateColor(vol: IVolume): string {
        if (vol.user_collection_data.state == 'Pre-Order') return '#f3b16b';
        else if (vol.user_collection_data.state == 'Shipping') return '#ff8d8d';
        else if (vol.user_collection_data.state == 'OOS') return '#a99eff';
        else if (vol.user_collection_data.state == 'Gift') return '#7dbbf3';
        else if (vol.user_collection_data.read) return '#2b9160';
        else if (vol.user_collection_data.state == 'Owned') return '#5fd19b';
        else if (vol.purchase_options.stock_status == 'Out of Stock') {
            return 'repeating-linear-gradient(135deg, #ebebeb, #ebebeb 4px, rgb(177 177 177) 5px, rgb(127 127 127) 8px)';

        }
        else if (vol.purchase_options.stock_status == 'Out of Print') return '#a3a3a3';
        else return '#ebebeb';
    }

}
