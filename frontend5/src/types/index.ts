export interface Bot {
  bot_id: number;
  name: string;
  is_launched: boolean;
}

export interface BotSetting {
  name: string;
  token: string;
  greeting_message: string;
  notifications: {
    on_new_user: boolean;
    on_product_sold: boolean;
    on_out_of_stock: boolean;
  };
}

export interface ButtonCondition {
  stage: string;
  equals: string;
  to: string;
}

export interface Button {
  text: string;
  to?: string;
  if?: ButtonCondition;
}

export interface Keyboard {
  back_button: boolean;
  buttons: Record<string, Button>;
}

export interface Product {
  title: string;
  description: string;
  price: number;
  image_url?: string;
}

export interface ProductType {
  product_type_id: number;
  name: string;
}

export interface BotProduct {
  product_id: number;
  product_type_id: number;
  file_id: string;
  is_sold: boolean;
}

export interface BaseStage {
  type: 'text' | 'image' | 'product';
  keyboard: Keyboard;
}

export interface TextStage extends BaseStage {
  type: 'text';
  text: string;
}

export interface ImageStage extends BaseStage {
  type: 'image';
  text: string;
  image: string;
}

export interface ProductStage extends BaseStage {
  type: 'product';
  product: Product;
}

export type Stage = TextStage | ImageStage | ProductStage;

export interface Dialog {
  stages: Record<string, Stage>;
}

export interface BotData {
  dialogs: Record<string, Dialog>;
}