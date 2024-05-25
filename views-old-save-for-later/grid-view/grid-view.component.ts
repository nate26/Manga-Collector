import { trigger, transition, style, animate } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { Component, EventEmitter } from '@angular/core';
import { IVolume } from '../../interfaces/iVolume.interface';
import { CollectionService } from '../../services/collection.service';

@Component({
    selector: 'app-grid-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './grid-view.component.html',
    styleUrl: './grid-view.component.css',
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
export class GridViewComponent {

    protected readonly volumes$ = this.collectionService.collectionAsVolume$;

    // put edit in service smh
    editVolume = new EventEmitter<IVolume>();

    constructor(private collectionService: CollectionService) { }

    edit(vol: IVolume) {
        this.editVolume.emit(vol)
    }

}
