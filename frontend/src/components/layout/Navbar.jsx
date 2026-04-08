import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useAuth } from "@/context/AuthContext"
import Logo from '@/assets/minet_light.png'

export default function Navbar() {
    const { isAuthenticated, logout } = useAuth()
    return (
        <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md shadow-sm">
            <div className="container flex h-16 items-center mx-auto px-4 max-w-7xl">

                {/* Section Logo */}
                <Link to="/" className="flex items-center space-x-3 transition-transform hover:scale-105">
                    <img src={Logo} alt="Logo Minet" className="h-10 w-10 object-contain" />
                    {/* Un magnifique texte en dégradé ! */}
                    <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent hidden sm:inline-block">
                        LocationMinet
                    </span>
                </Link>

                {/* Section Espace Droite */}
                <div className="flex flex-1 items-center justify-end space-x-4">
                    <nav className="flex items-center space-x-2">
                        {/* Un bouton "Ghost" (invisible tant qu'on ne le survole pas) pour le catalogue */}
                        <Button variant="ghost" asChild className="hidden text-muted-foreground hover:text-foreground sm:flex">
                            <Link to="/">Catalogue</Link>
                        </Button>

                        {/* 3. L'affichage Magique : Connecté OU Non connecté ? */}
                        {isAuthenticated ? (
                            <>
                                <Button asChild variant="ghost" className="hidden sm:flex text-muted-foreground hover:text-foreground">
                                    <Link to="/dashboard">Dashboard</Link>
                                </Button>
                                <Button onClick={logout} variant="outline" className="font-semibold shadow-md transition-transform hover:-translate-y-0.5">
                                    Déconnexion
                                </Button>
                            </>
                        ) : (
                            <Button asChild className="font-semibold shadow-md transition-transform hover:-translate-y-0.5">
                                <Link to="/login">Espace Asso</Link>
                            </Button>
                        )}
                    </nav>
                </div>
            </div>
        </header>
    )
}
