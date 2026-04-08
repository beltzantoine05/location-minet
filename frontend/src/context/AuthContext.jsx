import { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '@/api/client'; // On importe notre client pour parler au back !

// 1. Création du contexte (la "boîte")
const AuthContext = createContext();

// 2. Le composant "Provider" (le gérant du state)
export const AuthProvider = ({ children }) => {

    // On initialise le state avec le token qui se trouverait (peut-être) déjà dans le navigateur
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [asso, setAsso] = useState(null);
    const [loading, setLoading] = useState(true); // Est-ce qu'on est en train de vérifier qui il est ?

    // Ce useEffect se déclenche au chargement de l'app, et à chaque fois que la variable 'token' change
    useEffect(() => {
        if (token) {
            // Le token est là, on le sauvegarde dans le navigateur pour plus tard
            localStorage.setItem('token', token);

            // On fait un appel à l'API pour récupérer les infos de l'asso correspondante
            apiClient.get('/associations/me', {
                headers: {
                    Authorization: `Bearer ${token}` // On donne la clé passe-partout 
                }
            })
                .then((res) => {
                    setAsso(res.data); // On sauvegarde les infos de l'asso retournées par notre backend
                    setLoading(false); // Le chargement est terminé
                })
                .catch(() => {
                    // Erreur : le token est mauvais ou a expiré ! On nettoie tout.
                    setToken(null);
                    setAsso(null);
                    localStorage.removeItem('token');
                    setLoading(false);
                });
        } else {
            // Pas de token ? On nettoie tout pour être sûr.
            localStorage.removeItem('token');
            setAsso(null);
            setLoading(false);
        }
    }, [token]);

    // La fonction qui sera appelée quand on réussira à se connecter
    const login = (newToken) => {
        setToken(newToken);
    };

    // La fonction qui sera appelée pour se déconnecter
    const logout = () => {
        setToken(null);
        setAsso(null);
    };

    // On rend les données et nos fonctions accessibles à "tous les enfants" (l'app toute entière)
    return (
        <AuthContext.Provider value={{ token, asso, login, logout, isAuthenticated: !!token, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

// 3. Notre Hook "raccourci" pour s'en servir depuis n'importe où !
export const useAuth = () => useContext(AuthContext);
