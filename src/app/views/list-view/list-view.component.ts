import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { IManga } from 'src/app/interfaces/iManga.interface';

@Component({
    selector: 'app-list-view',
    templateUrl: './list-view.component.html',
    styleUrls: ['./list-view.component.css']
})
export class ListViewComponent implements OnInit {

    @Input()
    volumes$!: Observable<IManga[]>;

    @Output()
    editVolume = new EventEmitter<IManga>();

    constructor() { }

    ngOnInit(): void {
    }

    edit(vol: IManga) {
        this.editVolume.emit(vol)
    }

}
