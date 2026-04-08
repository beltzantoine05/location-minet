import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter, CardDescription } from "@/components/ui/card"
import { useAuth } from "@/context/AuthContext"

// Importe bien ton apiClient !
import apiClient from "@/api/client"
import Logo from "@/assets/minet_light.png"

export default function Login() {
    // 1. On crée nos "États" React pour stocker ce que tape l'utilisateur
    const [nom, setNom] = useState('')
    const [password, setPassword] = useState('')
    const [erreur, setErreur] = useState(null)
    const { login } = useAuth()

    const navigate = useNavigate()

    // 2. La fonction qui se lance quand on clique sur "Se connecter"
    const handleLogin = async (e) => {
        e.preventDefault() // Empêche la page de se rafraîchir
        setErreur(null) // On remet l'erreur à zéro à chaque essai

        try {
            // FastAPI demande un format spécifique (URLSearchParams)
            const formData = new URLSearchParams()
            formData.append('username', nom)
            formData.append('password', password)

            const response = await apiClient.post('/token', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })

            // 3. CA MARCHE ! On cache le token dans le navigateur
            const token = response.data.access_token
            login(token)

            console.log("Connecté avec succès !")
            // 4. On redirige vers le tableau de bord
            navigate('/dashboard')

        } catch (error) {
            console.error(error)
            setErreur("Nom d'association ou mot de passe incorrect")
        }
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">
            <Link to="/" className="mb-6 flex flex-col items-center gap-2 group">
                <img src={Logo} alt="Logo MiNET" className="w-14 h-14 transition-transform group-hover:scale-110" />
                <span className="font-extrabold text-xl tracking-tight text-primary">LocationMinet</span>
            </Link>

            <Card className="w-full max-w-md shadow-lg border-muted/60">
                <CardHeader className="space-y-1 text-center">
                    <CardTitle className="text-2xl font-bold tracking-tight">
                        Connexion Asso
                    </CardTitle>
                    <CardDescription className="text-sm">
                        Connecte-toi avec le nom de l'association.
                    </CardDescription>
                </CardHeader>

                <CardContent>
                    {/* On branche le onSubmit du formulaire avec notre fonction !! */}
                    <form className="space-y-6" onSubmit={handleLogin}>

                        <div className="space-y-2">
                            {/* On demande bien le Nom, pas l'email */}
                            <Label htmlFor="nom">Nom de l'association</Label>
                            <Input
                                id="nom"
                                type="text"
                                placeholder="BDE MiNET"
                                value={nom}
                                onChange={(e) => setNom(e.target.value)} // React "écoute" ce qui est tapé
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <Label htmlFor="password">Mot de passe</Label>
                            </div>
                            <Input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)} // Pareil ici
                                required
                            />
                        </div>

                        {/* On affiche le message d'erreur rouge s'il y a un soucis ! */}
                        {erreur && <p className="text-red-500 text-sm font-semibold">{erreur}</p>}

                        {/* Button de type 'submit' pour capter la validation ! */}
                        <Button type="submit" className="w-full font-semibold">
                            Se connecter
                        </Button>
                    </form>
                </CardContent>

                <CardFooter className="flex flex-col items-center justify-center gap-2 border-t pt-6 bg-muted/10 rounded-b-lg">
                    <p className="text-sm text-muted-foreground">
                        Ton association n'est pas encore inscrite ?
                    </p>
                    <Link to="/contact" className="text-sm font-semibold text-primary hover:underline">
                        Fais une demande d'accès
                    </Link>
                </CardFooter>
            </Card>
        </div>
    )
}
