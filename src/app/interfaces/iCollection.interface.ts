export interface ICollection {
  id?: string;
  temp_id?: string; // only for temp new volumes before saving
  user_id: string;
  isbn: string;
  state: string;
  cost: number;
  merchant: string;
  purchaseDate: string;
  giftToMe: boolean;
  read: boolean;
  tags: string[];
  inserted?: string;
  updated?: string;
}
