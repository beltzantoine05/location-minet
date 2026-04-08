import apiClient from "./client";

export const getItems = async () => {
    const response = await apiClient.get('/items/');
    return response.data
}

export const getAssociationItems = async (associationId) => {
    const response = await apiClient.get(`/associations/${associationId}/items`);
    return response.data
}

export const deleteItem = async (itemId) => {
    const response = await apiClient.delete(`/items/${itemId}`);
    return response.data
}

export const updateItem = async (itemId, data) => {
    const response = await apiClient.put(`/items/${itemId}`, data);
    return response.data
}

export const createItem = async (data) => {
    const response = await apiClient.post(`/items/`, data);
    return response.data
}

