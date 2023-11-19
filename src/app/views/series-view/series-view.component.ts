import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { IManga } from '../../interfaces/iManga.interface';
import { ISeriesEditionParsed } from '../../interfaces/iSeries.interface';

@Component({
    selector: 'app-series-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './series-view.component.html',
    styleUrl: './series-view.component.css'
})
export class SeriesViewComponent {

    @Input()
    series$!: Observable<ISeriesEditionParsed[]>;

    @Output()
    editVolume = new EventEmitter<IManga>();

    constructor() { }

    getVolumeStyle(vol: IManga) {
        const style = {
            background: '',
            color: '',
            border: '',
            'text-shadow': ''
        }
        if (vol.state == 'Pre-Order') style.background = '#f3b16b';
        else if (vol.state == 'Shipping') style.background = '#ff8d8d';
        else if (vol.state == 'OOS') style.background = '#a99eff';
        else if (vol.state == 'Gift') style.background = '#7dbbf3';
        else if (vol.read) style.background = '#2b9160';
        else if (vol.state == 'Owned') style.background = '#5fd19b';
        else if (vol.stock_status == 'Out of Stock') {
            style.background = 'repeating-linear-gradient(135deg, #ebebeb, #ebebeb 4px, rgb(177 177 177) 5px, rgb(127 127 127) 8px)';
            style['text-shadow'] = '0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff';
        }
        else if (vol.stock_status == 'Out of Print') style.background = '#a3a3a3';
        else style.background = '#ebebeb';



        if ((new Date(vol.release_date)) > (new Date())) style.color = '#e69138';

        if (vol.is_on_sale && !vol.purchaseDate) style.border = '3px solid rgb(219 85 85 / 60%)';
        return style;
    }

    edit(vol: IManga) {
        this.editVolume.emit(vol)
    }

}
