import { Component, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionDataService } from '../../services/data/collection-data.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop'
import { IVolume } from '../../interfaces/iVolume.interface';

interface TextEvent extends Event {
    target: EventTarget & { value: string };
}

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    volumes = signal<IVolume[]>([]);

    editing = signal(false);
    saveBatch = signal<{ index: number; field: string; value: Event; }[]>([]);

    displayVolumes = computed(() => {
        const vols = this.volumes();
        if (!vols) return [];
        const saveBatchState = this.saveBatch();
        return vols.map((volume, idx) => {
            const saveState = saveBatchState.find(s => s.index === idx);
            if (saveState) {
                const eventVal = (<TextEvent>saveState.value).target.value;
                const newVal = saveState.field === 'tags' ? eventVal.split(',') : (saveState.field === 'cost' ? parseFloat(eventVal) : eventVal);
                return { ...volume, user_collection_data: [{ ...volume.user_collection_data[0], [saveState.field]: newVal }] };
            }
            return volume;
        });
    });

    constructor(private collectionDataService: CollectionDataService) {
        this.collectionDataService.collectionVolumes$.pipe(
            takeUntilDestroyed()
        ).subscribe(volumes => {
            this.volumes.set(volumes);
        });
    }

    save(index: number, field: string, value: Event) {
        this.saveBatch.update(batch => {
            if (batch.some(b => b.index === index && b.field === field)) {
                // update existing if was previously saved
                return batch.map(b => b.index === index && b.field === field ? { ...b, value } : b);
            }
            // add save state
            return [...batch, { index, field, value }]
        })
    }

}
