import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, Button, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { auth } from './lib/firebase';
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  onAuthStateChanged,
  User 
} from 'firebase/auth';

// --- DİKKAT: IP ADRESİNİZİ VE PORTU KONTROL EDİN --- //
// Port numarasının 8000 olduğundan emin olun!
// Bunu başlatmadan önce python manage.py runserver 0.0.0.0:8000 ile django backendini başlat
// 172.20.10.3 olan kısmı kendi bilgisayarınızın IP adresi ile değiştir
const API_URL = 'http://172.20.10.3:8000'; 

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const handleSignUp = async () => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      Alert.alert('Kayıt Başarılı', `Hoş geldin ${userCredential.user.email}`);
    } catch (error: any) {
      Alert.alert('Kayıt Başarısız', error.message);
    }
  };

  const handleLogin = async () => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      Alert.alert('Giriş Başarılı', `Tekrar hoş geldin ${userCredential.user.email}`);
    } catch (error: any) {
      Alert.alert('Giriş Başarısız', error.message);
    }
  };

  const handleLogout = async () => {
    try {
      await auth.signOut();
      Alert.alert('Çıkış Yapıldı');
    } catch (error: any) {
      Alert.alert('Çıkış Başarısız', error.message);
    }
  };
  
  const testApiCall = async () => {
    if (!user) {
      return Alert.alert("Hata", "Bu işlemi yapmak için giriş yapmalısınız.");
    }
    
    try {
      const token = await user.getIdToken();
      const response = await fetch(`${API_URL}/api/profile/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      const responseText = await response.text();
      
      try {
        const data = JSON.parse(responseText);
        if (response.ok) {
          Alert.alert("API Başarılı", `Profil bilgisi bulundu: ${JSON.stringify(data)}`);
        } else {
          Alert.alert(
            "API Yanıtı (BU BİR BAŞARIDIR!)", 
            `Statü: ${response.status}\nMesaj: ${JSON.stringify(data)}`
          );
        }
      } catch (jsonError) {
        Alert.alert(
            "API Sunucu Hatası", 
            `Sunucu JSON yerine başka bir formatta yanıt verdi. Django terminalini kontrol edin.\n\nSunucu Yanıtı:\n${responseText.substring(0, 200)}...` // Yanıtın ilk 200 karakterini göster
        );
      }

    } catch (error: any) {
      Alert.alert("API Bağlantı Hatası", `Sunucuya bağlanılamadı. IP adresini (${API_URL}) ve Django sunucusunun çalıştığını kontrol ettin mi?\n\nDetay: ${error.message}`);
      console.error(error);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Yükleniyor...</Text>
      </View>
    );
  }

  if (user) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Hoş Geldin</Text>
        <Text style={styles.emailText}>{user.email}</Text>
        
        <View style={styles.buttonWrapper}>
          <Button title="Backend API'sini Test Et" onPress={testApiCall} />
        </View>

        <View style={styles.buttonWrapper}>
          <Button title="Çıkış Yap" onPress={handleLogout} color="#c0392b" />
        </View>

        <StatusBar style="auto" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Giriş Yap veya Kaydol</Text>

      <TextInput
        style={styles.input}
        placeholder="E-posta"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />

      <TextInput
        style={styles.input}
        placeholder="Şifre"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      
      <View style={styles.buttonContainer}>
        <Button title="Giriş Yap" onPress={handleLogin} />
        <Button title="Kaydol" onPress={handleSignUp} />
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 24,
    justifyContent: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
    color: '#333',
  },
  input: {
    height: 48,
    backgroundColor: '#fff',
    borderColor: '#ddd',
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 16,
    paddingHorizontal: 12,
    fontSize: 16,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  emailText: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
    color: '#555',
  },
  buttonWrapper: {
    marginTop: 10,
    borderRadius: 8,
    overflow: 'hidden',
  }
});