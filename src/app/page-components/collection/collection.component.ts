import { Component, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionDataService } from '../../services/data/collection-data.service';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop'
import { IVolume } from '../../interfaces/iVolume.interface';
import { ICollection } from '../../interfaces/iCollection.interface';

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
    saveBatch = signal<ICollection[]>([]);
    saved = signal<ICollection[]>([]);

    filterName = signal<string>('');
    filterCategory = signal<string>('');
    filterVolume = signal<string>('');
    filterCost = signal<string>('');
    filterMerchant = signal<string>('');
    filterPurchaseDate = signal<string>('');
    filterRead = signal<string>('');
    filterGiftToMe = signal<string>('');
    filterTags = signal<string>('');

    // separate filter and saved states for performance
    displayVolumes = computed(() => {
        const vols = this.volumes();
        if (!vols) return [];
        return vols
            .filter(volume => {
                const record = volume.user_collection_data[0];
                // check name
                return (!this.filterName() || (volume.name ?? '').toLowerCase().includes(this.filterName().toLowerCase()))
                    // check category
                    && (this.filterCategory() === '' || volume.category === this.filterCategory())
                    // check volume
                    && (!this.filterVolume() || volume.volume === this.filterVolume())
                    // check cost
                    && (!this.filterCost() || record.cost.toString() === this.filterCost())
                    // check merchant
                    && (this.filterMerchant() === '' || record.merchant === this.filterMerchant())
                    // check purchaseDate
                    && (!this.filterPurchaseDate() || (record.purchaseDate ?? '').toLowerCase().includes(this.filterPurchaseDate().toLowerCase()))
                    // check read
                    && (this.filterRead() === '' || record.read === (this.filterRead() === 'YES'))
                    // check giftToMe
                    && (this.filterGiftToMe() === '' || record.giftToMe === (this.filterGiftToMe() === 'YES'))
                    // check tags
                    && (!this.filterTags() || record.tags.join(',').toLowerCase().includes(this.filterTags().toLowerCase()));
            })
            .map(volume => {
                const editedState = this.saveBatch().find(record => record.id === volume.user_collection_data[0].id);
                const savedState = this.saved().find(record => record.id === volume.user_collection_data[0].id);
                const changed = editedState || savedState;
                if (changed) {
                    return { ...volume, user_collection_data: [changed], edited: Boolean(editedState) };
                }
                return { ...volume, edited: false };
            });
    });

    saveToCollection = computed(() => !this.editing() ? this.saveBatch() : []);
    saveToCollection$ = toObservable(this.saveToCollection).pipe(
        takeUntilDestroyed(),
        this.collectionDataService.saveToCollection
    ).subscribe({
        next: () => {
            console.log('The following records were saved: ', this.saveBatch());
            this.saved.update(batch => this.saveBatch().reduce((acc, record) => this.batchEdit(acc, record), batch));
            this.saveBatch.set([]);
        },
        error: () => this.editing.set(true)
    });

    constructor(private collectionDataService: CollectionDataService) {
        this.collectionDataService.collectionVolumes$.pipe(
            takeUntilDestroyed()
        ).subscribe(volumes => {
            this.volumes.set(volumes);
        });
    }

    edit(index: number, field: string, value: Event) {
        this.saveBatch.update(batch => {

            // get existing record
            const record = this.displayVolumes()[index].user_collection_data[0];

            // parse new value
            const eventVal = (<TextEvent>value).target.value;
            let parsedValue;
            if (field === 'tags') parsedValue = eventVal ? eventVal.split(',').map(t => t.trim()) : [];
            else if (field === 'cost') parsedValue = parseFloat(eventVal);
            else if (field === 'read' || field === 'giftToMe') parsedValue = eventVal === 'on';
            else parsedValue = eventVal;

            return this.batchEdit(batch, { ...record, [field]: parsedValue });
        })
    }

    batchEdit(batch: ICollection[], record: ICollection) {
        // update batch if record is already in batch
        if (batch.some(b => b.id === record.id)) {
            // update existing if was previously saved
            return batch.map(existingRecord => existingRecord.id === record.id ? record : existingRecord);
        }

        // add to batch if not already there
        return [...batch, record]
    }

    getEventVal(value: Event) {
        return (<TextEvent>value).target.value;
    }

}
