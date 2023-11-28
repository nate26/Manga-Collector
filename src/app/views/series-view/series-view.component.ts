import { CommonModule } from '@angular/common';
import { Component, EventEmitter } from '@angular/core';
import { IManga } from '../../interfaces/iManga.interface';
import { CollectionService } from '../../services/collection.service';
import { CdkTableModule } from '@angular/cdk/table';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { ISeriesEditionParsed } from '../../interfaces/iSeries.interface';
import { CoverImageSlideshowComponent } from '../../common/cover-image-slideshow/cover-image-slideshow.component';
import { FormsModule } from '@angular/forms';

export interface TableColumn {
    header: string;
    key: string;
    align: string;
    width?: string;
    style?: () => { [key: string]: string };
    render?: 'text' | 'image' | 'checkbox';
}

@Component({
    selector: 'app-series-view',
    standalone: true,
    imports: [CommonModule, FormsModule, CdkTableModule, MatButtonModule, MatCheckboxModule, CoverImageSlideshowComponent],
    templateUrl: './series-view.component.html',
    styleUrl: './series-view.component.css',
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ]
})
export class SeriesViewComponent {

    series$ = this.collectionService.collectionAsSeries$;

    expandedElement!: ISeriesEditionParsed | null;
    selectedVol!: IManga | null;

    seriesColumns: TableColumn[] = [
        {
            header: '',
            key: 'cover',
            align: 'center',
            width: '50px',
            render: 'image'
        },
        {
            header: 'Series',
            key: 'edition',
            align: 'left'
        },
        {
            header: 'Format',
            key: 'format',
            align: 'center',
            width: '100px'
        }
    ];
    seriesColumnKeys = this.seriesColumns.map(col => col.key);

    // put edit in service smh
    editVolume = new EventEmitter<IManga>();

    constructor(private collectionService: CollectionService) { }

    getVolumeStyle(vol: IManga) {
        const style = {
            background: '',
            color: 'black',
            border: '',
            'text-shadow': '',
            'box-shadow': ''
        }
        if (vol.state == 'Pre-Order') style.background = '#f3b16b';
        else if (vol.state == 'Shipping') style.background = '#ff8d8d';
        else if (vol.state == 'OOS') style.background = '#a99eff';
        else if (vol.state == 'Gift') style.background = '#7dbbf3';
        else if (vol.read) style.background = '#2b9160';
        else if (vol.state == 'Owned') style.background = '#8adab4';
        else if (vol.stock_status == 'Out of Stock') {
            style.background = 'repeating-linear-gradient(135deg, #ebebeb, #ebebeb 4px, rgb(177 177 177) 5px, rgb(127 127 127) 8px)';
            style['text-shadow'] = '0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff';
        }
        else if (vol.stock_status == 'Out of Print') style.background = '#a3a3a3';
        else style.background = '#ebebeb';

        if ((new Date(vol.release_date)) > (new Date())) style.color = '#e69138';

        if (vol.is_on_sale && !vol.purchaseDate) style.border = '3px solid rgb(219 85 85 / 60%)';

        if (this.selectedVol === vol) {
            style['box-shadow'] = '0px 0px 2px 2px #f5f5f5bf'
        }
        return style;
    }

    getAttr(item: ISeriesEditionParsed, column: TableColumn): unknown {
        return item[column.key as keyof ISeriesEditionParsed]
    }

    edit(vol: IManga) {
        this.editVolume.emit(vol)
    }

    setExpanded(row: ISeriesEditionParsed): void {
        if (this.expandedElement === row) {
            // clear expansion
            this.expandedElement = null;
            this.selectedVol = null;
        }
        else {
            // set expansion data
            this.expandedElement = this.expandedElement === row ? null : row;
            this.selectedVol = row.volumes.length > 0 ? row.volumes[0] : null;
        }
    }

}
