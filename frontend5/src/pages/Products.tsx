import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Trash2, Package } from 'lucide-react';
import { endpoints } from '../config/api';
import { fetchWithAuth } from '../utils/api';
import { ProductType, BotProduct } from '../types';

export default function Products() {
    const { botId } = useParams<{ botId: string }>();
    const [productTypes, setProductTypes] = useState<ProductType[]>([]);
    const [products, setProducts] = useState<BotProduct[]>([]);
    const [selectedType, setSelectedType] = useState<ProductType | null>(null);
    const [showSoldOnly, setShowSoldOnly] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchProductTypes = async () => {
        try {
            const response = await fetchWithAuth(endpoints.getAllProductTypes(Number(botId)));
            const data = await response.json();
            setProductTypes(data);
        } catch (error) {
            console.error('Error fetching product types:', error);
        }
    };

    const fetchProducts = async (typeId: number) => {
        try {
            const response = await fetchWithAuth(endpoints.getAllProducts(typeId));
            const data = await response.json();
            setProducts(data);
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    };

    useEffect(() => {
        fetchProductTypes();
    }, [botId]);

    const handleTypeSelect = async (type: ProductType) => {
        setSelectedType(type);
        await fetchProducts(type.product_type_id);
    };

    const handleUploadProduct = async () => {
        if (!selectedFile || !selectedType) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetchWithAuth(
                endpoints.uploadProduct(selectedType.product_type_id),
                {
                    method: 'POST',
                    body: formData,
                }
            );
            const data = await response.json();
            setProducts([...products, data]);
            setSelectedFile(null);
            setIsUploadModalOpen(false);
        } catch (error) {
            console.error('Error uploading product:', error);
        }
    };

    const handleDeleteProduct = async (productId: number) => {
        try {
            await fetchWithAuth(endpoints.deleteProduct(productId), {
                method: 'DELETE',
            });
            setProducts(products.filter((p) => p.product_id !== productId));
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    };

    const handleDeleteType = async (typeId: number) => {
        try {
            const response = await fetchWithAuth(endpoints.deleteProductType(typeId), {
                method: 'DELETE',
            });

            if (!response.ok) {
                const errorData = await response.json();
                setError(errorData.detail || 'Failed to delete product type');
                setTimeout(() => setError(null), 3000);
                return;
            }

            setProductTypes(productTypes.filter((t) => t.product_type_id !== typeId));
            if (selectedType?.product_type_id === typeId) {
                setSelectedType(null);
                setProducts([]);
            }
        } catch (error) {
            console.error('Error deleting product type:', error);
            setError('Failed to delete product type');
            setTimeout(() => setError(null), 3000);
        }
    };

    const filteredProducts = showSoldOnly
        ? products.filter((p) => p.is_sold)
        : products;

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold">Products</h1>
                </div>

                {error && (
                    <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
                        {error}
                    </div>
                )}

                <div className="grid grid-cols-4 gap-6">
                    {/* Product Types Sidebar */}
                    <div className="col-span-1 bg-white rounded-lg shadow-md p-4">
                        <h2 className="text-xl font-semibold mb-4">Product Types</h2>
                        <div className="space-y-2">
                            {productTypes.map((type) => (
                                <div
                                    key={type.product_type_id}
                                    className={`flex items-center justify-between p-2 rounded-md cursor-pointer ${
                                        selectedType?.product_type_id === type.product_type_id
                                            ? 'bg-blue-50 text-blue-600'
                                            : 'hover:bg-gray-50'
                                    }`}
                                    onClick={() => handleTypeSelect(type)}
                                >
                                    <span>{type.name}</span>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleDeleteType(type.product_type_id);
                                        }}
                                        className="p-1 text-gray-400 hover:text-red-500"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Products List */}
                    <div className="col-span-3 bg-white rounded-lg shadow-md p-4">
                        {selectedType ? (
                            <>
                                <div className="flex justify-between items-center mb-6">
                                    <div className="space-x-4">
                                        <h2 className="text-xl font-semibold inline-block">
                                            {selectedType.name} Products
                                        </h2>
                                        <label className="inline-flex items-center">
                                            <input
                                                type="checkbox"
                                                checked={showSoldOnly}
                                                onChange={(e) => setShowSoldOnly(e.target.checked)}
                                                className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                                            />
                                            <span className="ml-2 text-sm text-gray-600">
                        Show sold only
                      </span>
                                        </label>
                                    </div>
                                    <button
                                        onClick={() => setIsUploadModalOpen(true)}
                                        className="flex items-center gap-2 bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
                                    >
                                        Upload Product
                                    </button>
                                </div>

                                <div className="grid grid-cols-3 gap-4">
                                    {filteredProducts.map((product) => (
                                        <div
                                            key={product.product_id}
                                            className="border rounded-lg p-4 relative"
                                        >
                                            <div className="flex items-start justify-between">
                                                <Package size={24} className="text-gray-600" />
                                                <button
                                                    onClick={() => handleDeleteProduct(product.product_id)}
                                                    className="text-gray-400 hover:text-red-500"
                                                >
                                                    <Trash2 size={20} />
                                                </button>
                                            </div>
                                            <div className="mt-2">
                                                <p className="text-sm text-gray-600">
                                                    ID: {product.product_id}
                                                </p>
                                                <p className="text-sm text-gray-600 truncate" title={product.file_id}>
                                                    File: {product.file_id}
                                                </p>
                                                <span
                                                    className={`inline-block mt-2 px-2 py-1 text-xs rounded-full ${
                                                        product.is_sold
                                                            ? 'bg-red-100 text-red-800'
                                                            : 'bg-green-100 text-green-800'
                                                    }`}
                                                >
                          {product.is_sold ? 'Sold' : 'Available'}
                        </span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </>
                        ) : (
                            <div className="text-center text-gray-500 py-8">
                                Select a product type to view products
                            </div>
                        )}
                    </div>
                </div>

                {/* Upload Product Modal */}
                {isUploadModalOpen && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                        <div className="bg-white p-6 rounded-lg w-96">
                            <h2 className="text-2xl font-bold mb-4">Upload Product</h2>
                            <input
                                type="file"
                                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                                className="w-full mb-4"
                            />
                            <div className="flex justify-end gap-2">
                                <button
                                    onClick={() => {
                                        setIsUploadModalOpen(false);
                                        setSelectedFile(null);
                                    }}
                                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={handleUploadProduct}
                                    disabled={!selectedFile}
                                    className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:bg-green-300"
                                >
                                    Upload
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}